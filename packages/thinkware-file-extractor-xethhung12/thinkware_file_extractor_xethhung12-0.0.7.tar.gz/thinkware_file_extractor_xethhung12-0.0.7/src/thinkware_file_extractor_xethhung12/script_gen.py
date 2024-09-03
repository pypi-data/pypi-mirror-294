from os.path import abspath


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