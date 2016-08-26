#ecoding:utf-8
import sys
import MySQLdb
import json
import traceback
import re
reload(sys)
sys.setdefaultencoding("utf-8")
# pattern = re.compile(r'<a.*?">')
# rootdir = '/Users/bjhl/Documents/'
# filename = sys.argv[1]
# fw = open(rootdir+filename+'.remove_a','a')
# for line in open(rootdir+filename):
#     line = line.strip().replace('</a>','')
#     for url in pattern.findall(line):
#         line = line.replace(url,'')
#     fw.write(line+'\n')
#     fw.flush()
# fw.close()

#当一行过长时,去掉re.S
s = u'<strong>诗词成就</strong><br/>　　<a target=\"_blank\" href=\"http://tool.liuxue86.com/shiren_view_9b9cc243ac9b9cc2/\">李白</a>的<a target=\"_blank\" href=\"http://tool.liuxue86.com/shici_view_9a04be43ac9a04be/\">乐府</a>、歌行及<a target=\"_blank\" href=\"http://tool.liuxue86.com/shici_view_9a3a3143ac9a3a31/\">绝句</a>成就为最高。其歌行，完全打破诗歌创作的一切固有格式，空无依傍，笔法多端，达到了任随性之而变幻莫测、摇曳多姿的神奇境界。李白的绝句自然明快，飘逸潇洒，能以简洁明快的语言表达出无尽的情思。在盛唐诗人中，<a target=\"_blank\" href=\"http://tool.liuxue86.com/shiren_view_9b9cd243ac9b9cd2/\">王维</a>、<a target=\"_blank\" href=\"http://tool.liuxue86.com/shiren_view_9b9d8843ac9b9d88/\">孟浩然</a>长于五绝，<a target=\"_blank\" href=\"http://tool.liuxue86.com/shiren_view_9b9d9b43ac9b9d9b/\">王昌龄</a>等<a target=\"_blank\" href=\"http://tool.liuxue86.com/shici_view_9bb4ea43ac9bb4ea/\">七绝</a>写得很好，兼长五绝与七绝而且同臻极境的，只有李白一人。<br/>　　李白的诗雄奇飘逸，艺术成就极高。他讴歌祖国山河与美丽的自然风光，风格雄奇奔放，俊逸清新，富有浪漫主义精神，达到了内容与艺术的完美统一。他被<a target=\"_blank\" href=\"http://tool.liuxue86.com/shiren_view_9b9e3843ac9b9e38/\">贺知章</a>称为“谪<a target=\"_blank\" href=\"http://tool.liuxue86.com/shici_view_999e5f43ac999e5f/\">仙人</a>”，其诗大多为描写山水和抒发内心的情感为主。李白的诗具有“笔落惊<a target=\"_blank\" href=\"http://tool.liuxue86.com/shici_view_9b91c043ac9b91c0/\">风雨</a>，诗成泣鬼神”的艺术魅力，这也是他的诗歌中最鲜明的艺术特色。李白的诗富于自我表现的主观抒情色彩十分浓烈，<a target=\"_blank\" href=\"http://tool.liuxue86.com/shici_view_9bcbf943ac9bcbf9/\">感情</a>的表达具有一种排山倒海、一泻千里的气势。他与<a target=\"_blank\" href=\"http://tool.liuxue86.com/shiren_view_9b9cc143ac9b9cc1/\">杜甫</a>并称为“大李杜”，（<a target=\"_blank\" href=\"http://tool.liuxue86.com/shiren_view_9b9cc643ac9b9cc6/\">李商隐</a>与<a target=\"_blank\" href=\"http://tool.liuxue86.com/shiren_view_9b9cd943ac9b9cd9/\">杜牧</a>并称为“小李杜”）。<br/>　　李白诗中常将想象、夸张、比喻、拟人等手法综合运用，从而造成神奇异彩、瑰丽动人的意境，这就是李白的浪漫主义诗作给人以豪迈奔放、飘逸若仙的原因所在。<br/>　　李白的诗歌对后代产生了极为深远的影响。中唐的<a target=\"_blank\" href=\"http://tool.liuxue86.com/shiren_view_9b9df343ac9b9df3/\">韩愈</a>、<a target=\"_blank\" href=\"http://tool.liuxue86.com/shiren_view_9b9cd543ac9b9cd5/\">孟郊</a>、<a target=\"_blank\" href=\"http://tool.liuxue86.com/shiren_view_9b9d8543ac9b9d85/\">李贺</a>，宋代的<a target=\"_blank\" href=\"http://tool.liuxue86.com/shiren_view_9b9cfb43ac9b9cfb/\">苏轼</a>、<a target=\"_blank\" href=\"http://tool.liuxue86.com/shiren_view_9b9ce743ac9b9ce7/\">陆游</a>、<a target=\"_blank\" href=\"http://tool.liuxue86.com/shiren_view_9b97c443ac9b97c4/\">辛弃疾</a>，明清的<a target=\"_blank\" href=\"http://tool.liuxue86.com/shiren_view_9b9cbd43ac9b9cbd/\">高启</a>、<a target=\"_blank\" href=\"http://tool.liuxue86.com/shiren_view_9b9d4943ac9b9d49/\">杨'
print re.sub('<a[^>]+>','',s)