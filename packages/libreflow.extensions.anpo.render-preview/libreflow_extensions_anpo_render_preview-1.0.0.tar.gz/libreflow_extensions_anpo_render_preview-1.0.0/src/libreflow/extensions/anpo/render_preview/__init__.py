import os
import subprocess
import platform
from kabaret import flow
from kabaret.flow.object import _Manager
from libreflow.baseflow.file import TrackedFile, RevealInExplorer

from . import _version
__version__ = _version.get_versions()['version']


class RenderPreview(RevealInExplorer):
    ICON = ('icons.gui','picture')
    _MANAGER_TYPE = _Manager
    _file = flow.Parent()

    def allow_context(self,context):
        return (context
                and self._file.format.get() in ['mov','mp4']
                and self._file.get_head_revision() is not None)

    def get_target_path(self):
        source_path = self._file.get_head_revision().get_path()
        
        name_format = f'{self._file.complete_name.get()}_preview'

        ffmpeg_exe = self.root().project().admin.project_settings.ffmpeg_path.get()
        webm_output_path = os.path.join(os.path.dirname(source_path), name_format +'.webm')
        thumb_output_path = os.path.join(os.path.dirname(source_path), name_format + '.jpeg')

        ffmpeg_args = ['ffmpeg.exe', '-i', source_path]

        webm_output_args = ffmpeg_args + ['-vf', '"scale=-1:256"', webm_output_path,'-y']
        thumb_output_args = ffmpeg_args + ['-frames:v', '1' ,'-vf', '"scale=-1:512"', thumb_output_path,'-y']
        webm_output_args =' '.join(webm_output_args)
        thumb_output_args = ' '.join(thumb_output_args)

        proc_webm = subprocess.run(webm_output_args, check=True, shell=platform.system() == 'Windows')
        proc_thumb = subprocess.run(thumb_output_args, check=True, shell=platform.system() == 'Windows')

        return os.path.dirname(source_path)


def render_preview(parent):
    if isinstance(parent, TrackedFile):
        r = flow.Child(RenderPreview)
        r.name = 'render_preview'
        r.index = 34
        return r

def install_extensions(session):
    return {
        "render_preview": [
            render_preview,
        ]
    }
