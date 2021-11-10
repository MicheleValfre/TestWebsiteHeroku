#EVENT TYPES
EVENT_TYPES = [
    ("Tournament","Tournament"),
    ("Foundraising","Foundraising")
]

def getType(t):
    if t == "T":
        return EVENT_TYPES[0][0]
    elif t == "F":
        return EVENT_TYPES[1][0]
    return ""

#Calendar stuff


monthToStr = {
  1:"Jan",
  2:"Feb",
  3:"Mar",
  4:"Apr",
  5:"May",
  6:"Jun",
  7:"Jul",
  8:"Aug",
  9:"Sep",
  10:"Oct",
  11:"Nov",
  12:"Dic"
}
