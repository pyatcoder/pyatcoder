from argparse import Namespace
from typing import TextIO, Dict, Any, Optional

import toml

from pyatcoder.config.etc_config import EtcConfig


def _update_config_dict(target_dic: Dict[str, Any], update_dic: Dict[str, Any]):
    return {
        **target_dic,
        **dict((k, v) for k, v in update_dic.items() if v is not None)
    }


class Config:

    def __init__(self,
                 etc_config: EtcConfig = EtcConfig()
                 ):
        self.etc_config = etc_config

    @classmethod
    def load(cls, fp: TextIO, args: Optional[Namespace] = None):
        """
        :param fp: .toml file's file pointer
        :param args: command line arguments
        :return: Config instance
        """
        config_dic = toml.load(fp)
        etc_config_dic = config_dic.get('etc', {})

        if args:
            etc_config_dic = _update_config_dict(etc_config_dic,
                                                 dict(
                                                     download_without_login=args.without_login,
                                                     save_no_session_cache=args.save_no_session_cache,
                                                 ))

        return Config(
            etc_config=EtcConfig(**etc_config_dic)
        )
