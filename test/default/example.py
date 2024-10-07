__COLORS__ = True
__CLEAR__ = False

class devCFG2:
    doClear: bool = False

class devCFG:
    doClear: bool = True
    allowDev: bool = False
    allowMods: bool = False
    checkVersion: bool = True
    saveCFG: bool = True
    loadCFG: bool = True

def codeInit():
    global restart, fileInfo, threads, exceptionBuffer, loadedSoundpack
    global devMode, godMode, passThrough
    restart = False
    godMode = False
    devMode = True
    passThrough = False
    threads = {'ptime': False, 'rpc': False}
    fileInfo = {'log': [None, None], 'music': [None, None, None]}
    exceptionBuffer = []
    loadedSoundpack = None

def classInit():
    global ACHS, GRAMMAR, DATA, ROOMS, OBJECTS, HIERARCHY, SPECIAL_ROOMS

    class ACHS:
        normal: dict
        aside: dict
        bside: dict

    class GRAMMAR:
        singular: list[str]
        nouns: list[str]

    class DATA:
        shapes: list[str]
        mats: list[str]
        tools: list[str]
        menus: list[str]
        rooms: list[str]

        @property
        def recipes():
            return DATA.shapes + DATA.tools

    class ROOMS:
        map: dict[str, list]
        alt: dict[str, list]

    class OBJECTS:
        drinks: list[str]
        foods: list[str]
        gemstones: list[str]
        minerals: list[str]
        ingots: list[str]
        materials: list[str]
        smelteables: list[str]
        equipables: list[str]
        consumables: list[str]
        sellables: list[str]

        @property
        def get_consumables(self):
            return self.drinks + self.foods

    class HIERARCHY:
        axe: dict
        pickaxe: dict
        hammer: dict
        backpack: dict
        watch: dict
        mallet: dict

        def get(self, tool):
            try:
                getattr(self, tool)
            except Exception:
                return

    class SPECIAL_ROOMS:
        bed: list[str]
        clock: list[str]
        trash: list[str]

def varsInit():
    global carStats, achDesc, toolHierarchy
    carStats = {}
    achDesc = {'normal': {}, 'aside': {}, 'bside': {}}
    toolHierarchy = {'axe': {None: 0}, 'pickaxe': {None: 0}, 'hammer': {None: 0}, 'backpack': {None: 0}, 'watch': {None: 0}, 'mallet': {None: 0}}
    classInit()