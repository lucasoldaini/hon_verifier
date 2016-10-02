import subprocess
import os

class HONVerifier(object):
    def __init__(self,
                 candgen_path='hon_hash_candidates.js',
                 hlist_path='listeMD5.txt',
                 hon_base_url='https://www.hon.ch/HONcode/?'):
        self.candgen_path = candgen_path
        with file(hlist_path) as hlf:
            hlist = [tuple(line.split()) for line in hlf.read().split('\n')
                     if len(line.strip()) > 0]
            self.hashlist = {h: (hon_base_url + p)
                             for h, p in hlist}

    def check_url(self, url):
        proc = subprocess.Popen([('./' + self.candgen_path), url],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        msg_out, msg_err = proc.communicate()
        if len(msg_err.strip()) > 0:
            raise OSError(msg_err)
        cands = msg_out.strip().split()
        result = [(self.hashlist[cand] if cand in self.hashlist else None)
                  for cand in cands]
        return filter(lambda x: x, result)


if __name__ == '__main__':
    import sys
    honv = HONVerifier()
    try:
        print honv.check_url(sys.argv[1])
    except IndexError:
        print honv.check_url('http://www.webmd.com/anxiety-panic/default.htm')
        print honv.check_url('http://www.pacemakerclub.com/public/jpage'
                             '/1/p/story/a/storypage/sid/20657/content.do')

