class EtcConfig:

    def __init__(self,
                 download_without_login: str = False,
                 save_no_session_cache: bool = False,
                 in_example_format: str = "{}.txt",
                 out_example_format: str = "out{}.txt",
                 workspace_dir: str = "~/atcoder-workspace/",
                 lang: str = "python"
                 ):
        self.download_without_login = download_without_login
        self.save_no_session_cache = save_no_session_cache
        self.in_example_format = in_example_format
        self.out_example_format = out_example_format
        self.workspace_dir = workspace_dir
        self.lang = lang
