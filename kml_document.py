
template_kml_document = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><kml xmlns=\"http://www.opengis.net/kml/2.2\" xmlns:gx=\"http://www.google.com/kml/ext/2.2\" xmlns:kml=\"http://www.opengis.net/kml/2.2\" xmlns:atom=\"http://www.w3.org/2005/Atom\"><Document><name>{}</name><open>{}</open>{}</Document></kml>"
template_kml_folder = "<Folder><name>{}</name><open>{}</open>{}</Folder>"
template_kml_line = "<Placemark><name>{}</name><visibility>{}</visibility><description>{}</description><styleUrl>{}</styleUrl><LineString><coordinates>{}</coordinates></LineString></Placemark>"
template_kml_point = "<Placemark><name>{}</name><visibility>{}</visibility><description>{}</description><styleUrl>{}</styleUrl><Point><coordinates>{},{},0</coordinates></Point></Placemark>"
default_style_line = "<Style id=\"line\"><LineStyle><color>ffffff55</color><width>2</width></LineStyle></Style>"
default_style_point = "<Style id=\"point\"><IconStyle><Icon><href>http://maps.google.com/mapfiles/kml/paddle/grn-blank.png</href></Icon><hotSpot x=\"32\" y=\"1\" xunits=\"pixels\" yunits=\"pixels\"/></IconStyle><LabelStyle><color>00ffffff</color></LabelStyle><ListStyle><ItemIcon><href>http://maps.google.com/mapfiles/kml/paddle/grn-blank-lv.png</href></ItemIcon></ListStyle></Style>"
default_style_point_no_label = "<Style id=\"point_no_label\"><IconStyle><Icon><href>http://maps.google.com/mapfiles/kml/paddle/grn-blank.png</href></Icon><hotSpot x=\"32\" y=\"1\" xunits=\"pixels\" yunits=\"pixels\"/></IconStyle><ListStyle><ItemIcon><href>http://maps.google.com/mapfiles/kml/paddle/grn-blank-lv.png</href></ItemIcon></ListStyle></Style>"

class kml_document:

    def __init__(self, name='', is_open=True):
        self.name = name
        self.is_open = is_open
        self.document_root = []

    def add_child(self, child):
        self.document_root.append(child)

    def write_to_file(self, filename):
        children = "".join(str(c) for c in self.document_root)
        document = template_kml_document.format(
            self.name,
            self.is_open,
            default_style_line +
            default_style_point +
            default_style_point_no_label +
            children
        )
        with open(filename, "w") as file:
            print(document, file=file)

class kml_folder:

    def __init__(self, name='', is_open=False):
        self.name = name
        self.is_open = is_open
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        children = "".join(str(c) for c in self.children)
        return template_kml_folder.format(self.name, self.is_open, children)

class kml_line:

    def __init__(self, name='', visibility=True, description=''):
        self.name = name
        self.visibility = visibility
        self.description = description
        self.style = "#line"
        self.coordinates = []

    def add_coordinate(self, longitude, latitude):
        self.coordinates.append([longitude, latitude])

    def __str__(self):
        coordinates = ",0 ".join(str(c[0]) + "," + str(c[1]) for c in self.coordinates) + ",0 "
        return template_kml_line.format(
            self.name,
            self.visibility,
            self.description,
            self.style,
            coordinates
        )

class kml_point:

    def __init__(self, longitude, latitude, name='', visibility=True, description='', label=True):
        self.longitude = longitude
        self.latitude = latitude
        self.name = name
        self.visibility = visibility
        self.description = description
        if label:
            self.style = "#point_no_label"
        else:
            self.style = "#point"

    def __str__(self):
        return template_kml_point.format(
            self.name,
            self.visibility,
            self.description,
            self.style,
            self.longitude,
            self.latitude
        )