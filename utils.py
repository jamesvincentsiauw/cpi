def get_xpath_value(tree, xpath, return_as_list=False):
    try:
        value = tree.xpath(xpath)

        if len(value) == 0:
            return None
        else:
            if not return_as_list:
                return value[0]
            else:
                return value
    except:
        return None
