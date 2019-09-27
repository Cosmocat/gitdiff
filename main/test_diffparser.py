import unittest
import diffparser

class TestDiffParser(unittest.TestCase):
    
    def test_parseDescriptor(self):
        self.assertEqual(diffparser.parseDescriptor('@@ -1,3 +1,4 @@'), [1, 1])
        self.assertEqual(diffparser.parseDescriptor('@@ -0,0 +1 @@'), [0, 1])
        self.assertEqual(diffparser.parseDescriptor('@@-1,3@@'), 'Unable to parse descriptor')

    def test_parseChunks(self):
        self.chunks = [
            {
                'descriptor': '@@ -1,8 +1,9 @@ ', 
                'content': [
                    ' #include "cache.h" ', 
                    ' #include "walker.h" ', 
                    '-int cmd_http_fetch(int argc, const char **argv, const char *prefix) ', 
                    '+int main(int argc, const char **argv) ', 
                    ' { ', '+       const char *prefix; ', 
                    '        struct walker *walker; ', 
                    '        int commits_on_stdin = 0; ', 
                    '        int commits; '
                ]
            }, 
            {
                'descriptor': '@@ -18,6 +19,8 @@', 
                'content': 
                [
                    ' int cmd_http_fetch(int argc, const char **argv, const char *prefix) ', 
                    '        int get_verbosely = 0; ', 
                    '        int get_recover = 0; ', 
                    '+       prefix = setup_git_directory(); ', 
                    '+ ', 
                    '        git_config(git_default_config, NULL); ', 
                    '        while (arg < argc && argv[arg][0] == \'-\') {'
                ]
            }
        ]
        self.parsedChunks = [
            {'lineContent': ' #include "cache.h" ', 'linenumNew': 1, 'linenumOld': 1}, 
            {'lineContent': ' #include "walker.h" ', 'linenumNew': 2, 'linenumOld': 2}, 
            {'linechangeInd': '-', 'lineContent': 'int cmd_http_fetch(int argc, const char **argv, const char *prefix) ', 'linenumOld': 3}, 
            {'linechangeInd': '+', 'lineContent': 'int main(int argc, const char **argv) ', 'linenumNew': 4}, 
            {'lineContent': ' { ', 'linenumNew': 5, 'linenumOld': 5}, 
            {'linechangeInd': '+', 'lineContent': '       const char *prefix; ', 'linenumNew': 6}, 
            {'lineContent': '        struct walker *walker; ', 'linenumNew': 7, 'linenumOld': 7}, 
            {'lineContent': '        int commits_on_stdin = 0; ', 'linenumNew': 8, 'linenumOld': 8}, 
            {'lineContent': '        int commits; ', 'linenumNew': 9, 'linenumOld': 9}, 
            {'lineContent': ' int cmd_http_fetch(int argc, const char **argv, const char *prefix) ', 'linenumNew': 19, 'linenumOld': 18}, 
            {'lineContent': '        int get_verbosely = 0; ', 'linenumNew': 20, 'linenumOld': 19}, 
            {'lineContent': '        int get_recover = 0; ', 'linenumNew': 21, 'linenumOld': 20}, 
            {'linechangeInd': '+', 'lineContent': '       prefix = setup_git_directory(); ', 'linenumNew': 22}, 
            {'linechangeInd': '+', 'lineContent': ' ', 'linenumNew': 23}, 
            {'lineContent': '        git_config(git_default_config, NULL); ', 'linenumNew': 24, 'linenumOld': 23}, 
            {'lineContent': "        while (arg < argc && argv[arg][0] == '-') {", 'linenumNew': 25, 'linenumOld': 24}
        ]
        self.assertEqual(diffparser.parseChunks(self.chunks), self.parsedChunks)


if __name__ == '__main__':
    unittest.main()