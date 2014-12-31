#!/usr/bin/env python2.7
import sys
import time
import traceback
import Queue
import threading
import signal

import triangle
import shows
import util

import cherrypy

class ShowRunner(threading.Thread):
    def __init__(self, model, queue, max_showtime=1000):
        super(ShowRunner, self).__init__(name="ShowRunner")
        self.model = model
        self.queue = queue

        self.running = True
        self.max_show_time = max_showtime
        self.show_runtime = 0

        # map of names -> show ctors
        self.shows = dict(shows.load_shows())
        self.randseq = shows.random_shows()

        # current show object & frame generator
        self.show = None
        self.framegen = None

        # current show parameters

        # show speed multiplier - ranges from 0.5 to 2.0
        # 1.0 is normal speed
        # lower numbers mean faster speeds, higher is slower
        self.speed_x = 1.0

    def status(self):
        if self.running:
            return "Running: %s (%d seconds left)" % (self.show.name, self.max_show_time - self.show_runtime)
        else:
            return "Stopped"

    def check_queue(self):
        msgs = []
        try:
            while True:
                m = self.queue.get_nowait()
                if m:
                    msgs.append(m)

        except Queue.Empty:
            pass

        if msgs:
            for m in msgs:
                self.process_command(m)

    def process_command(self, msg):
        if isinstance(msg,basestring):
            if msg == "shutdown":
                self.running = False
                print "ShowRunner shutting down"
            elif msg == "clear":
                self.clear()
                time.sleep(2)
            elif msg.startswith("run_show:"):
                self.running = True
                show_name = msg[9:]
                self.next_show(show_name)
            elif msg.startswith("inc runtime"):
                self.max_show_time = int(msg.split(':')[1])

        elif isinstance(msg, tuple):
            # osc message
            # ('/1/command', [value])
            print "OSC:", msg

            (addr,val) = msg
            addr = addr.split('/z')[0]
            val = val[0]
            assert addr[0] == '/'
            (ns, cmd) = addr[1:].split('/')
            if ns == '1':
                # control command
                if cmd == 'next':
                    self.next_show()
                elif cmd == 'previous':
                    if self.prev_show:
                        self.next_show(self.prev_show.name)
                elif cmd == 'speed':
                    self.speed_x = speed_interpolation(val)
                    print "setting speed_x to:", self.speed_x

                pass
            elif ns == '2':
                # show command
                if self.show_params:
                    self.show.set_param(cmd, val)

        else:
            print "ignoring unknown msg:", str(msg)

    def clear(self):
        self.model.clear()


    def next_show(self, name=None):
        s = None
        if name:
            if name in self.shows:
                s = self.shows[name]
            else:
                print "unknown show:", name

        if not s:
            print "choosing random show"
            s = self.randseq.next()

        self.clear()
        self.prev_show = self.show

        self.show = s(self.model)
        print "next show:" + self.show.name
        self.framegen = self.show.next_frame()
        self.show_params = hasattr(self.show, 'set_param')
        self.show_runtime = 0

    def get_next_frame(self):
        "return a delay or None"
        try:
            return self.framegen.next()
        except StopIteration:
            return None

    def run(self):
        if not (self.show and self.framegen):
            self.next_show()

        while self.running:
            try:
                self.check_queue()

                d = self.get_next_frame()
                self.model.go()
                if d:
                    real_d = d * self.speed_x
                    time.sleep(real_d)
                    self.show_runtime += real_d
                    if self.show_runtime > self.max_show_time:
                        print "max show time elapsed, changing shows"
                        self.next_show()
                else:
                    print "show is out of frames, waiting..."
                    time.sleep(2)
                    self.next_show()

            except Exception:
                print "unexpected exception in show loop!"
                traceback.print_exc()
                self.next_show()


class TriangleServer(object):
    def __init__(self, triangle_model, args):
        self.args = args
        self.triangle_model = triangle_model

        self.queue = Queue.LifoQueue()

        self.runner = None

        self.running = False
        self._create_services()

    def _create_services(self):
        # Show runner
        self.runner = ShowRunner(self.triangle_model, self.queue, args.max_time)
        if args.shows:
            print "setting show:", args.shows[0]
            self.runner.next_show(args.shows[0])

    def start(self):
        if self.running:
            print "start() called, but triangle is already running!"
            return

        try:
            self.runner.start()

            self.running = True
        except Exception, e:
            print "Exception starting Triangles!"
            traceback.print_exc()

    def stop(self):
        if self.running: # should be safe to call multiple times
            try:
                # ShowRunner is shut down via the message queue
                self.queue.put("shutdown")

                self.running = False
            except Exception, e:
                print "Exception stopping Triangles!"
                traceback.print_exc()

    def go_headless(self, app):
        "Run with web interface"
#        print "Running without web interface"
#        try:
#            while True:
#                time.sleep(999) # control-c breaks out of time.sleep

        port = 9991
        config = {
            'global': {
                    'server.socket_host': '0.0.0.0',
                    'server.socket_port' : port
                    }
                }
        cherrypy.quickstart(TriWeb(app),
                '/',
                config=config)
#        except KeyboardInterrupt:
#            print "Exiting on keyboard interrupt"

        self.stop()

class TriWeb(object):
    def __init__(self, app):
        self.app = app
        self.runner = self.app.runner
        self.show_names = [s[0] for s in shows.load_shows()]
        pass

    @cherrypy.expose
    def index(self):
        ret_html = "Shows:<br>"
        for i in self.show_names:
            ret_html += "<a href=/next_show?show_name=%s > %s </a><br>" % (i,i)

        ret_html += """
        <form action="/show_time">
            <input type='text' name='show_time'></input>
            <input type='submit' value='set show time'></input>
        </form>
        """
        return ret_html

    @cherrypy.expose
    def next_show(self, show_name=None):
        self.runner.next_show(show_name)
        ret_html = "<a href=/>HOME</a><script>setTimeout(function(){window.location='/'},3000)</script>"
        return ret_html

    @cherrypy.expose
    def show_time(self, show_time=float(180)):
        self.runner.max_show_time = float(show_time)
        ret_html = "next show will be %s seconds <script>setTimeout(function(){window.location='/'},3000)</script>" % show_time
        return ret_html


    @cherrypy.expose
    def kill(self):
        cherrypy.engine.exit()
        self.app.stop()
        import sys
        sys.exit()

if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Baaahs Light Control')

    parser.add_argument('--max-time', type=float, default=float(180),
                        help='Maximum number of seconds a show will run (default 180)')

    # Simulator must run to turn on lights
    # parser.add_argument('--simulator',dest='simulator',action='store_true')

    parser.add_argument('--list', action='store_true', help='List available shows')
    parser.add_argument('shows', metavar='show_name', type=str, nargs='*',
                        help='name of show (or shows) to run')

    args = parser.parse_args()

    if args.list:
        print "Available shows:"
        print ', '.join([s[0] for s in shows.load_shows()])
        sys.exit(0)

    sim_host = "localhost"
    sim_port = 4444

    print "Using Triangle Simulator at %s:%d" % (sim_host, sim_port)

    from model.simulator import SimulatorModel
    model = SimulatorModel(sim_host, port=sim_port)
    full_triangles = triangle.load_triangles(model)

    app = TriangleServer(full_triangles, args)
    try:
        app.start() # start related service threads
        app.go_headless(app)

    except Exception, e:
        print "Unhandled exception running Triangles!"
        traceback.print_exc()
    finally:
        app.stop()
