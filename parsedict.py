import xml.etree.cElementTree as et

def harvest(element, match):
    return set(x.text for x in element.findall(match))
def package(element, match, func):
    return list(map(func, element.findall(match)))

class entry:
    def __init__(self, element):
        # entry has an id#, 1+ reading, 0+ kanji, 1+ sense
        assert element.tag == 'entry'
        self.readings = package(element, 'r_ele', reading)
        self.variants = package(element, 'k_ele', kanji)
        # senses
        assert self.readings
        self.value = self.readings[0].value if not self.variants else self.variants[0].value
    def __str__(self):
        return self.value
        
        
class reading:
    def __init__(self, element):
        # reading has value, may indicate no kanji, 0+ restrictions/info/priority
        assert element.tag == 'r_ele'
        self.value = element.findtext('reb')        
        self.nokanji = element.find('re_nokanji')
        self.restriction = harvest(element, 're_restr')        
        self.priority = harvest(element, 're_pri')
        self.info = harvest(element, 're_inf')
        assert self.value is not None

class kanji:
    def __init__(self, element):
        # kanji has value, may have priority and irregularity info.
        assert element.tag == 'k_ele'
        self.value = element.findtext('keb')
        self.priority = harvest(element, 'ke_pri')
        self.info = harvest(element, 'ke_inf')
        assert self.value is not None
        
tree = et.parse('JMdict_e')

root = tree.getroot()
            
entries = list(map(entry, root))

# priorities: news1/2, ichi1/2, spec1/2, nf01-48

# info: phonetic readings, irregular okurigana/kana, out-dated..

#ki = set(x for e in entries for k in e.variants for x in k.info)
#ri = set(x for e in entries for k in e.readings for x in k.info)

# Note:
# - seems to be no jplt info
# - seems to be no ruby structure