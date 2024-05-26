from ParseBuilder.BaseParser import parser


class PyBuilder:
    def build(self):
        with open("Parser.py", "w", encoding="utf-8") as file:
            file.write(parser)
        file.close()
