import os, sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as anima
import time
from engineer.SQLbeast.str2type import str2mat
import sqlite3

db = "TEMP_MESH.db"

def animation(A, f, interval, title='Temperature profile over time   [K]', name='animationsss.mp4'):
    sys.stdout.write('\r GENERATING VIDEO...')
    ttt = time.time()
    Writer = anima.writers['ffmpeg']

    writer = Writer(fps=10, metadata=dict(artist='Me'), bitrate=1800)
    fig = plt.figure()
    plt.title(title)
    try:
        T = f.T0 + [f.Tg] + [f.Ti] + [f.To]
    except AttributeError:
        T = f.T
    try:
        ln = plt.imshow(str2mat(A[0]), cmap=plt.get_cmap('jet'), vmin=min(T), vmax=max(T))
    except:
        ln = plt.imshow(A[0], cmap=plt.get_cmap('jet'), vmin=min(T), vmax=max(T))
    itr = len(A)
    def update(i):
        sys.stdout.write('\r GENERATING VIDEO...\t{}%'.format(round(i*100/itr)))
        if isinstance(A[i], str):
            ln.set_array(str2mat(A[i]))
        else:
            ln.set_array(A[i])
        return [ln]
    ani = FuncAnimation(fig, update, frames=range(len(A)), interval=interval, blit=True)
    plt.colorbar()
    sys.stdout.write('\r GENERATING VIDEO... DONE! {}\n'.format(time.time() - ttt))
    return writer, ani

def animation_from(dbname):
    conn = sqlite3.connect(db)
    curs = conn.cursor()
    for row in curs.execute("SELECT * FROM %s " % dbname):
        pass