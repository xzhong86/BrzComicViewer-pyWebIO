
# default config
global_cfg = dict(
    books_dir  = "./books",
    unpack_dir = "./books",
    unpack_pattern = "book-u{index}-{hash}",
    unpack_update_info = True,
    quiet = True,
)

class Options:
    def __init__(self, cfg):
        for key, val in cfg.items():
            setattr(self, key, val)

def mergeConfig(default, _new):
    cfg = { }
    for key in default:
        item = _new[key] if key in _new else default[key]
        cfg[key] = item
    return cfg

opt = Options(global_cfg)
def set(_new):
    global global_cfg
    global opt
    cfg = mergeConfig(global_cfg, _new)
    global_cfg = cfg
    opt = Options(cfg)

def get():
    return global_cfg
