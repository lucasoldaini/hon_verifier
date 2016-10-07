import subprocess


class HONVerifier(object):
    def __init__(self,
                 candgen_path='hon_verifier/hon_hash_candidates.js',
                 hlist_path='hon_verifier/listeMD5.txt',
                 hon_base_url='https://www.hon.ch/HONcode/?'):
        self.candgen_path = candgen_path
        with open(hlist_path) as hlf:
            hlist = [tuple(line.split()) for line in hlf.read().split('\n')
                     if len(line.strip()) > 0]
            self.hashlist = {h: (hon_base_url + p) for h, p in hlist}

    def check_url(self, *urls):
        if len(urls) == 0:
            raise RuntimeError('No URL provided.')

        proc = subprocess.Popen(
            [('./' + self.candgen_path)] + list(urls),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        msg_out, msg_err = proc.communicate()
        if len(msg_err.strip()) > 0:
            raise OSError(msg_err.decode('utf-8'))

        cands_group = [
            gr.strip().split()
            for gr in msg_out.strip().decode('utf-8').split('\n\n')
        ]

        results = []
        for cands in cands_group:

            result = [(self.hashlist[cand] if cand in self.hashlist else None)
                      for cand in cands]
            results.append(len(list(filter(lambda x: x, result))) > 0)

        if len(results) == 1:
            return results[0]
        else:
            return results


if __name__ == '__main__':
    import sys
    honv = HONVerifier()
    try:
        print(honv.check_url(sys.argv[1]))
    except IndexError:
        u1 = 'http://www.webmd.com/anxiety-panic/default.htm'
        u2 = 'https://apple.com'
        # print(honv.check_url('http://www.webmd.com/anxiety-panic/default.htm'))
        # print(honv.check_url('http://www.pacemakerclub.com/public/jpage'
        #                      '/1/p/story/a/storypage/sid/20657/content.do'))

        import time
        IT = 100

        start = time.time()
        ch = [u1 if i % 2 else u2 for i in range(IT)]
        honv.check_url(*ch)
        print(time.time() - start)

        start = time.time()
        for i in range(IT):
            honv.check_url(u1 if i % 2 else u2)
        print(time.time() - start)


