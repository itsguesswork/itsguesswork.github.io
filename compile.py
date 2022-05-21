import json
import os
import shutil

def create_fresh_directory_named(directory):
    shutil.rmtree(directory)
    os.mkdir(directory)
    shutil.copytree("routes/" + directory + "/images", directory + "/images")
    # shutil.copy("routes/" + directory + "/style.css", directory + "/style.css")

def template_from(route, template, directory):
    for property in route.keys():
        if type(route[property]) is list:
            with open("routes/" + directory + "/" + property + ".html") as html_file:
                sub_template = html_file.read()
                sub_page = ""
                for sub_route in route[property]:
                    sub_page += template_from(sub_route, sub_template, directory)
                template = template.replace("{{" + property + "}}", sub_page)
        else:
            template = template.replace("{{" + property + "}}", route[property])
    return template

create_fresh_directory_named("listen")
html_file = open("routes/listen/template.html")
template = html_file.read()
html_file.close()
with open("routes/listen/pages.json") as file:
    listenRoutes = json.load(file)
    for route in listenRoutes:
        new_page = template_from(route, template, "listen")
        with open("listen/" + route["slug"] + ".html", "w") as output:
            output.write(new_page)