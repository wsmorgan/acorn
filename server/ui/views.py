from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
import os

def _get_colors(n):
    """Returns n unique and "evenly" spaced colors for the backgrounds
    of the projects.

    Args:
        n (int): The number of unique colors wanted.

    Returns:
        colors (list of str): The colors in hex form.
    """

    import matplotlib.pyplot as plt
    import matplotlib
    
    # cmap = plt.cm.get_cmap('Set2')
    cmap = plt.cm.get_cmap('Accent')
    this_color = 0.0
    interval = 1.0/n
    colors = []
    while len(colors) < n:
        colors.append(matplotlib.colors.rgb2hex(cmap(this_color)[:3]))
        this_color += interval

    return colors

def _color_variant(hex_color, brightness_offset=1):
    """Takes a color like #87c95f and produces a lighter or darker variant.
    Code adapted from method proposed by Chase Seibert at:
    http://chase-seibert.github.io/blog/2011/07/29/python-calculate-lighterdarker-rgb-colors.html.
    
    Args:
        hex_color (str): The original hex color.
        brightness_offset (int): The amount to shift the color by.

    Returns:
        new_color (str): The new hex color variant.

    Raises:
        Exception: if the len of the hex_color isn't the appropriate length (7).
    """
    if len(hex_color) != 7:
        raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
    rgb_hex = [hex_color[x:x+2] for x in [1, 3, 5]]
    new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
    new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int] # make sure new values are between 0 and 255
    # hex() produces "0x88", we want just "88"
    new_color = "#"
    for i in new_rgb_int:
        if len(hex(i)[2:]) == 2:
            new_color += hex(i)[2:]
        else:
            new_color += hex(i)[2:] + "0"

    return new_color


def _make_projcet_list(path):
    """Returns a dictionaries in which each project is a key and the
    tasks are stored as a list within that dictionaly element.
    
    Args:
        path (str): The path to the folder containing the *.json files.
    
    Returns:
        projects (list of dict): A dictionary in which each project is a key 
          containing a list of it's tasks.
    """

    proj = []
    projects = {}
    file_list = os.listdir(path)
    for files in file_list:
        if files.split(".")[0] not in proj and 'json' in files:
            proj.append(files.split(".")[0])

    # get the background color for each project.
    colors = _get_colors(len(proj))
    p_c = 0
    for p in proj:
        tasks = {}
        temp = [x.split(".")[1] for x in file_list if p in x]
        hue_range = [i - len(temp)/2 for i in range(len(temp))]
        hues = [_color_variant(colors[p_c],brightness_offset=hue*25) for hue in hue_range]
        h_c = 0
        for t in temp:
            tasks[t] = hues[h_c]
            h_c += 1
        tasks["hex_color"] = colors[p_c]
        projects[p] = tasks
        p_c += 1
        
    return projects
        

def index(request):
    context = RequestContext(request)
    projects = request.session.get('projects')
    if not projects:
        path = "/Users/wileymorgan/Dropbox/acorn"
        projects = _make_projcet_list(path)

    
    context_dict = {'projects':projects}
    return render_to_response("ui/index.html", context_dict, context)

def about(request):
    context = RequestContext(request)
    projects = request.session.get('projects')
    if not projects:
        path = "/Users/wileymorgan/Dropbox/acorn"
        projects = _make_projcet_list(path)

    context_dict = {'projects':projects}
    return render_to_response("ui/about.html", context_dict, context)

def dailyLog(request):
    context = RequestContext(request)
    projects = request.session.get('projects')
    if not projects:
        path = "/Users/wileymorgan/Dropbox/acorn"
        projects = _make_projcet_list(path)
    
    context_dict = {'projects':projects}
    return render_to_response("ui/daily_log.html", context_dict, context)
