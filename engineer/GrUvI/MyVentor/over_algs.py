POINTOS = 2     # Point OffSet:  distance from point center that still allow select/highlight
CIRCLEOS = 10   # Circle OffSet: distance from circle outline that still allow select/highlight
LINEOS = 5      # Line OffSet:   distance from line that still allow select/highlight

def over_point(points, evt):
    """
    returns whether or not mouse is over a point
    :param points: 2 coordinates [x1, y1, x2, y2] of the point which is actually a small oval
    :param evt: mouse event
    :return:
    """
    if (points[0] - POINTOS <= evt.x <= points[2] + POINTOS and
        points[1] - POINTOS <= evt.y <= points[3] + POINTOS):
        return True
    return False

def over_circle(radius, center, evt):
    """
    Checks if mouse is over circle
    :param radius: radius of circle
    :param center: center coordinate of circle
    :param evt: mouse event
    :return:
    """
    rsq = (center[0]-evt.x)**2 + (center[1]-evt.y)**2
    if (radius-CIRCLEOS)**2 <= rsq <= (radius+CIRCLEOS)**2:
        return True
    return False

def over_line(points, evt):
    """
    Checks whether mouse is over a line
    :param points: end points of line [x1, y1, x2, y2]
    :param evt: mouse event
    :return:
    """
    # y = (y2-y1)/(x2-x1)x + y1
    #
    #
    #
    check = (points[3]-points[1])/(points[2]-points[0])*evt.x + points[1]
    if check - LINEOS <= evt.y <= check + LINEOS:
        return True
    return False
