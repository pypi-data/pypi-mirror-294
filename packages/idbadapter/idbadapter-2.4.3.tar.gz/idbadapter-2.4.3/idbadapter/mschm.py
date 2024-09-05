from typing import Type, Union
import json
from contextlib import contextmanager
from sqlalchemy.exc import ResourceClosedError

import pandas as pd

from sqlalchemy.orm import scoped_session

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select, delete, update, text as sql_text

from sqlalchemy import create_engine
from .models import MSCHMModel, ResModel
from .models import S7Model, MSModel


from functools import lru_cache

class MschmAdapter:
    def __init__(self, url, echo=False):
        self.engine = create_engine(url, echo=echo)
        self.session_factory = sessionmaker(bind=self.engine)

        self.mschm_models = {}
        self.mro_models = {}
        self.res_models = {}

    def get_links_history(self):
        with self.engine.begin() as context:
            stmt = sql_text('select * from sampo_historical_data')
            return pd.read_sql(stmt, context)

    def update_links_history(self, df: pd.DataFrame):
        with self.engine.begin() as context:
            df.to_sql(name='sampo_historical_data', con=context, if_exists='replace')

    def get_all_models_names(self):
        perf_models = self.__execute_query(select(MSModel))
        res_models = self.__execute_query(select(ResModel))
        result = {
            "res_models_names": [k.name for k in res_models],
            "perf_models_names": [k.name for k in perf_models]
        }
        return result

    def save_res_model(self, name, model, measurement_type=None) -> None:
        models_to_write = []
        current = self.get_res_model(name, measurement_type)
        if current is not None:
            self.__execute_query(delete(ResModel).where(ResModel.name == name,
                                                       ResModel.measurement_type == measurement_type), True)
        data = json.dumps(model)
        models_to_write.append(ResModel(name=name,
                                        data=data,
                                        measurement_type=measurement_type))
        self.__save([models_to_write])

    def get_res_model(self, name: str, measurement_type: str | None = None) -> dict | None:
        if measurement_type is None:
            result: list[ResModel] = self.__execute_query(
                select(ResModel).where(ResModel.name == name)
            )
            return {k.measurement_type: k.data for k in result}
        key = (name, measurement_type)
        if key in self.res_models:
            return self.res_models[key]
        elif len(self.res_models) == 0:
            result: list[ResModel] = self.__execute_query(
                select(ResModel))
            self.res_models = {(k.name, k.measurement_type): json.loads(k.data) for k in result}
            try:
                return self.res_models[key]
            except KeyError:
                return None
        else:
            return None

    def save_perf_model(self, model, measurement_type=None):
        models_to_write = []
        for work_name, work_data in model.items():
            current = self.get_perf_model(work_name, measurement_type)
            if current is not None:
                self.__execute_query(delete(MSModel).where(MSModel.name == work_name,
                                                           MSModel.measurement_type == measurement_type), True)
            data = json.dumps(work_data)
            models_to_write.append(MSModel(name=work_name,
                                           data=data,
                                           measurement_type=measurement_type))
        self.__save([models_to_write])

    def get_perf_model(self, name, measurement_type=None):
        if measurement_type is None:
            result: list[MSModel] = self.__execute_query(
                select(MSModel).where(MSModel.name == name)
            )
            return {k.measurement_type: k.data for k in result}
        key = (name, measurement_type)
        if key in self.mschm_models:
            return self.mschm_models[key]
        elif len(self.mschm_models) == 0:
            result: list[MSModel] = self.__execute_query(
                select(MSModel))
            self.mschm_models = {(k.name, k.measurement_type): json.loads(k.data) for k in result}
            try:
                return self.mschm_models[key]
            except KeyError:
                return None
        else:
            print(f"model with name {name} not found!")
            return

    def save_mro_model(self, model, measurement_type=None):
        models_to_write = []
        for name, data in model.items():
            # check if model in database
            current = self.get_s7_model(name)
            if current is not None:
                self.__execute_query(delete(S7Model).where(S7Model.name==name), True)
            data = json.dumps(data)
            models_to_write.append(S7Model(name=name,
                                           data=data))
        self.__save([models_to_write])

    def get_mro_model(self, name):
        if name in self.mro_models:
            return self.mro_models[name]
        elif len(self.mro_models) == 0:
            result: list[S7Model] = self.__execute_query(
                select(S7Model))
            self.mro_models = {k.name: json.loads(k.data) for k in result}
            return self.mro_models[name]

    def __get_last_id_from_db(self, cls: Type[MSCHMModel]):
        query = sql_text(f"select max(id) from {cls.__tablename__}")
        last_id = self.__execute_query(query)
        last_id = last_id[0]
        if last_id is None:
            return 0
        return last_id

    def __get_basic_objects(self, cls):
        query = select(cls)
        result = self.__execute_query(query)
        return {(o.name, o.measurement): o for o in result}

    def __save(self, collections: list[list]):
        for collection in collections:
            self.__save_to_database(collection)

    def __save_to_database(self, collection):
        with self.__get_session() as context:
            context.add_all(collection)
            context.commit()

    def __get_last_id(self, collection: list, cls: Type[MSCHMModel]):
        if len(collection):
            return max([o.id for o in collection])
        else:
            last_id = self.__get_last_id_from_db(cls)
            return 0 if last_id is None else last_id

    def __execute_query(self, query, commit=False) -> list:
        with self.__get_session() as context:
            result = context.execute(query)
            try:
                result = result.scalars().all()
            except ResourceClosedError:
                pass
            if commit:
                context.commit()

        return result

    @contextmanager
    def __get_session(self):
        session = scoped_session(self.session_factory)
        try:
            yield session
        finally:
            session.close()
