import re
def md2commands(desc):
    ret = ""
    if desc is not None :
        string_split_re=r"(<b>.*)</b>|(<i>.*)</i>|(<p>)|</p>|(<img\ src=\".+\">)|(<img\ alt=.+)/>|(<a\ href=\".+)</a>|</a>"
        # parenthesis keep the separators. We do not need the terminators like /b ,/i

        s=re.split(string_split_re, desc)
        for x in s:
            #print(x)
            if x is not None :
                x= x.replace("\n", " ")
                if len(x)>0 :
                    if x !=  " " :
                        #print("split element: ", x)
                        if x == "<p>" :
                            ret += "\npara "  # new line
                        else :
                            if  re.match("<i>", x) :
                                ret += "\nitalic " + re.match("<i>(.*)", x).group(1) # italic
                            else :
                                if re.match("<b>", x) :
                                    ret += "\nbolt " + re.match("<b>(.*)", x).group(1)  # bolt mode
                                else :
                                    if re.match("<img src=", x)  :
                                        filename = re.match(r"<img src=\"\s*(.+)\"", x).group(1)
                                        ret += f"\nimage \"{filename}\""  #.format(filename) # image
                                    else:
                                        if re.match("<img alt", x)  :
                                            [text, filename] = re.findall(r"<img alt=\"(.+)\" src=\"(.+)\"", x)[0]
                                            ret += "\nimage " + "\"" + filename  + "\"" + text  # image
                                        else:
                                            if re.match("<a href=", x)  :
                                                [url, text]= re.findall("<a href=\"(.+)\">(.*)", x)[0]
                                                ret += "\nhlink " + " \"" + url  + "\" " + text  # url
                                            else :
                                                ret += "\ntext " + x.replace("\n", " ") # remove potential newline
    return ret

if __name__ == '__main__':
    MD_TEST_STRING = r"""
<p>Register description of Atmel XMEGA AU's SPI controller
Transcribed from original manual as an example exercise:
http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-8331-8-and-16-bit-AVR-Microcontroller-XMEGA-AU_Manual.pdf
(test image name)
<a href="example.jpg">Turbo Encabulator</a>
test
<img src=" P:/nerdl/test/ic.png">
test1
<a href="http://www.accellera.org">http://www.accellera.org</a>
test2
<a href="http://www.accellera.org">Accellera url description</a>
test3</p>
<p>test
<b>test bold </b> <i>test italic</i></p>
"""

    print (MD_TEST_STRING)
    print(md2commands(MD_TEST_STRING))
