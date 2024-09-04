import requests as rq
import json
from tai_alphi.handlers import TeamsHandler
from tai_alphi.config import AlphiConfig
from tai_alphi.adaptative_cards import CardTemplate
from tai_alphi.loggers import AlphiLogger
from datetime import datetime


class Alphi(AlphiConfig):

    def __init__(self, config_file: str):

        super().__init__(config_file)
        self.date = datetime.today()
        self.time = datetime.now()
        self._logger_failed = {} # Para teams
        self._loggers = {}

    def get_logger(self, logger_name: str) -> AlphiLogger:
        if logger_name in self._loggers:
            alphi_logger = self._loggers.get(logger_name)
        else:
            alphi_logger = AlphiLogger(config= self.config, name=logger_name,
                              nosqlDB_conn_config = self.nosqlDB_conn_config, logtail_token = self.logtail_token)
            self._loggers[logger_name] = alphi_logger

        return alphi_logger

    def teams_alert(self, webhook, proyecto, pipeline, notify_to):

        for l in self._loggers:         
            handlers = self._loggers.get(l).handlers
            for h in handlers:
                if isinstance(h, TeamsHandler):
                    teams_handler = h
                    logger_name = l
                    break

        logs = teams_handler.get_queue_contents()

        if "ERROR" in logs or "CRITICAL" in logs:
            self._logger_failed[logger_name] = True
        
        if not self._logger_failed.get(logger_name):
            notify_to=[]

        template = CardTemplate(
            failed=self._logger_failed.get(logger_name),
            proyecto=proyecto,
            pipeline=pipeline,
            date=self.date,
            time=self.time,
            logs=logs,
            notify_to=notify_to,
        )

        card = template.get_card('card1')

        json_object = json.dumps(card)
        rq.post(webhook, json_object)
    
    # # def _set_teams_alert_on_exit(self):
