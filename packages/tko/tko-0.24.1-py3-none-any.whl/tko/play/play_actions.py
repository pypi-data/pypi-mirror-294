from .keys import GuiKeys
from ..game.game import Game
from ..game.cluster import Cluster
from ..game.quest import Quest
from ..game.task import Task
from ..game.graph import Graph
from .opener import Opener
from ..run.basic import Success
from typing import List
from ..settings.settings import Settings
from tko.cmds.cmd_down import CmdDown

from ..settings.rep_settings import languages_avaliable, RepData
from ..down.down import DownProblem
from ..util.sentence import Sentence, Token
from .fmt import Fmt


from .floating import Floating
from .floating_manager import FloatingManager
from .flags import Flag, Flags, FlagsMan
from .tasktree import TaskTree
from ..cmds.cmd_run import Run
from ..run.param import Param
from .gui import Gui

import os
import tempfile
import subprocess

class PlayActions:

    def __init__(self, fman: FloatingManager, rep: RepData, rep_alias:str, tree: TaskTree, game: Game, opener: Opener, gui: Gui):
        self.app = Settings().app
        self.settings = Settings()
        self.fman = fman
        self.rep = rep
        self.rep_alias = rep_alias
        self.tree = tree
        self.game = game
        self.opener = opener
        self.graph_opened: bool = False
        self.gui = gui

    def gen_graph_path(self) -> str:
        return os.path.join(self.app._rootdir, self.rep_alias, "graph.png")
        

    def open_link_without_stdout_stderr(self, link: str):
        outfile = tempfile.NamedTemporaryFile(delete=False)
        subprocess.Popen("python3 -m webbrowser -t {}".format(link), stdout=outfile, stderr=outfile, shell=True)

    def open_link(self):
        obj = self.tree.get_selected()
        if isinstance(obj, Task):
            task: Task = obj
            if task.link.startswith("http"):
                try:
                    self.open_link_without_stdout_stderr(task.link)
                except Exception as _:
                    pass
            self.fman.add_input(
                Floating("v>")
                .set_header(" Abrindo link ")
                .put_text("\n " + task.link + " \n")
                .warning()
            )
        elif isinstance(obj, Quest):
            self.fman.add_input(
                Floating("v>")
                .put_text("\nEssa é uma missão.")
                .put_text("\nVocê só pode abrir o link")
                .put_text("de tarefas.\n")
                .error()
            )
        else:
            self.fman.add_input(
                Floating("v>")
                .put_text("\nEsse é um grupo.")
                .put_text("\nVocê só pode abrir o link")
                .put_text("de tarefas.\n")
                .error()
            )

    def generate_graph(self):
        try:
            Graph(self.game).set_path(self.gen_graph_path()).set_opt(False).generate()
            path = self.gen_graph_path()
            # self.fman.add_input(Floating().put_text(f"\nGrafo gerado em\n {path} \n"))
            if not self.graph_opened:
                self.opener.open_files([path])
                self.graph_opened = True
        except FileNotFoundError as _:
            self.gui.config.gen_graph = False
            self.fman.add_input(Floating().error()
                                .put_text("")
                                .put_sentence(Sentence().add("Instale o ").addf("r", "graphviz").add(" para poder gerar os grafos"))
                                .put_text("")
                                )

    def down_task(self):

        lang = self.rep.get_lang() 
        obj = self.tree.items[self.tree.index_selected].obj
        if isinstance(obj, Task) and obj.key in obj.title:
            task: Task = obj
            down_frame = (
                Floating("v>").warning().set_ljust_text().set_header(" Baixando tarefa ")
            )
            down_frame.put_text(f"\ntko down {self.rep_alias} {task.key} -l {lang}\n")
            self.fman.add_input(down_frame)

            def fnprint(text):
                down_frame.put_text(text)
                down_frame.draw()
                Fmt.refresh()
            CmdDown.execute(self.rep_alias, task.key, lang, self.settings, fnprint, self.game)
        else:
            if isinstance(obj, Quest):
                self.fman.add_input(
                    Floating("v>")
                    .put_text("\nEssa é uma missão.")
                    .put_text("\nVocê só pode baixar tarefas.\n")
                    .error()
                )
            elif isinstance(obj, Cluster):
                self.fman.add_input(
                    Floating("v>")
                    .put_text("\nEsse é um grupo.")
                    .put_text("\nVocê só pode baixar tarefas.\n")
                    .error()
                )
            else:
                self.fman.add_input(
                    Floating("v>").put_text("\nEssa não é uma tarefa de código.\n").error()
                )
    
    def select_task(self):
        rootdir = self.app._rootdir
        
        obj = self.tree.items[self.tree.index_selected].obj

        if isinstance(obj, Quest) or isinstance(obj, Cluster):
            self.tree.toggle(obj)
            return

        rep_dir = os.path.join(rootdir, self.rep_alias)
        task: Task = obj
        if not task.is_downloadable():
            self.open_link()
            return
        if not task.is_downloaded_for_lang(rep_dir, self.rep.get_lang()):
            self.down_task()
            return
        return self.run_selected_task(task, rep_dir)
        
    def run_selected_task(self, task: Task, rep_dir: str):
        path = os.path.join(rep_dir, task.key)
        run = Run([path], None, Param.Basic())
        run.set_lang(self.rep.get_lang())
        run.set_opener(self.opener)
        run.set_autorun(False)
        if Flags.images.is_true():
            run.set_curses(True, Success.RANDOM)
        else:
            run.set_curses(True, Success.FIXED)
        run.set_task(task)

        run.build_wdir()
        if not run.wdir.has_solver():
            msg = Floating("v>").error()
            msg.put_text("\nNenhum arquivo de código na linguagem {} encontrado.".format(self.rep.get_lang()))
            msg.put_text("Arquivos encontrados na pasta:\n")
            folder = run.wdir.get_autoload_folder()
            file_list = [file for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]
            for file in file_list:
                msg.put_text(file)
            msg.put_text("")
            self.fman.add_input(msg)
            return
        return run.execute