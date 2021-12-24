import xml.etree.ElementTree as ET
from datetime import datetime


def read_config_xml(file_name):

    """
    Function for config.xml reading using ElementTree
    """

    tree = ET.parse(file_name)
    root = tree.getroot()

    data = []
    player_name = ""

    data.append(int(root[0].find("item[@name='FPS']").text))
    data.append(int(root[0].find("item[@name='HEIGHT']").text))
    data.append(int(root[0].find("item[@name='WIDTH']").text))
    data.append(int(root[0].find("item[@name='BORDER_WIDTH']").text))
    data.append(int(root[0].find("item[@name='BORDER_HEIGHT']").text))
    data.append(int(root[0].find("item[@name='REQ_SHIP_SIZE']").text))
    data.append(int(root[0].find("item[@name='MAX_SCORE']").text))
    data.append(int(root[0].find("item[@name='MOUSE_POS_X']").text))
    data.append(int(root[0].find("item[@name='MOUSE_POS_Y']").text))
    data.append(int(root[0].find("item[@name='RESTRICT_X']").text))
    data.append(int(root[0].find("item[@name='RESTRICT_Y']").text))
    data.append(int(root[0].find("item[@name='MARGIN']").text))
    data.append(int(root[0].find("item[@name='SIZE']").text))
    player_name = root[0].find("item[@name='PLAYER_NAME']").text

    return (data, player_name)


def write_results_xml(winner, game_time, guesses, p_score, c_score):

    """
    This function writes game results into GameResults.xml file,
    overwriting it each game session.
    """

    date_time = datetime.now().isoformat(sep=" ")

    data = ET.Element("data")
    results = ET.SubElement(data, "results")
    item1 = ET.SubElement(results, "item")
    item2 = ET.SubElement(results, "item")
    item3 = ET.SubElement(results, "item")
    item4 = ET.SubElement(results, "item")
    item5 = ET.SubElement(results, "item")
    item6 = ET.SubElement(results, "item")
    item1.set("name", "date_time")
    item2.set("name", "game_time")
    item3.set("name", "winner")
    item4.set("name", "guesses")
    item5.set("name", "player_score")
    item6.set("name", "computer_score")
    item1.text = date_time
    item2.text = game_time
    item3.text = winner
    item4.text = str(guesses)
    item5.text = str(p_score)
    item6.text = str(c_score)

    results_data = ET.tostring(data)
    file = open("GameResults.xml", "wb")
    file.write(results_data)
