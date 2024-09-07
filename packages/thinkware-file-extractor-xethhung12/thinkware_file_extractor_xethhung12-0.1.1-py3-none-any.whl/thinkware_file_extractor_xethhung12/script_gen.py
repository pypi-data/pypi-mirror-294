import os
from os.path import abspath, exists, isdir


def gen_merge_script(source, dest, prefix, suffix, dest_file_name):
    source = abspath(source)
    source = source[0:-1] if source.endswith("/") else source
    dest = abspath(dest)
    dest = dest[0:-1] if dest.endswith("/") else dest
    dest_file=f"{dest}/{dest_file_name}"
    dest_mp4_file=f"{dest}/{dest_file_name}.mp4"

    replaced_source=source.replace("/","\\/")+"\\/"
    return f"""


##### Generate merge script 
rm -f {dest_file} {dest_mp4_file}
ls -al {source} | grep -o {prefix}_.*_{suffix}.MP4 | sed 's/^/file {replaced_source}/' > {dest_file}
ffmpeg -f concat -safe 0 -i {dest_file} -vcodec copy -acodec copy {dest_mp4_file}
"""

def gen_copy_script(source, dest):
    if not exists(source):
        raise FileNotFoundError
    if not isdir(source):
        raise NotADirectoryError

    source = str(abspath(source))
    source = source[0:-1] if source.endswith("/") else source
    source_cont_rec=f"{source}/cont_rec"
    source_evt_rec=f"{source}/evt_rec"
    source_manual_rec=f"{source}/manual_rec"
    source_motion_timelapse_rec=f"{source}/montion_timelapse_rec"
    source_parking_rec=f"{source}/parking_rec"

    os.makedirs(dest,exist_ok=True)
    dest = abspath(dest)
    dest = dest[0:-1] if dest.endswith("/") else dest
    dest_cont_rec=f"{dest}/cont_rec"
    dest_evt_rec=f"{dest}/evt_rec"
    dest_manual_rec=f"{dest}/manual_rec"
    dest_motion_timelapse_rec=f"{dest}/montion_timelapse_rec"
    dest_parking_rec=f"{dest}/parking_rec"

    def script_from_to(src, dest):
        return f"""
echo copy from `{src}` to `{dest}`
rm -fr {dest}
cp -r {src} {dest}
"""

    script_gen = "\n".join([script_from_to(s, d) for s,d in [
        [source_cont_rec, dest_cont_rec],
        [source_evt_rec, dest_evt_rec],
        [source_manual_rec, dest_manual_rec],
        [source_motion_timelapse_rec, dest_motion_timelapse_rec],
        [source_parking_rec, dest_parking_rec]
    ]])
    return script_gen




