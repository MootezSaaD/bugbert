from TextEmbedding import TextEmbedding
from elastic_search.Searcher.Searcher import Searcher


query = "This is the 100th Etext file presented by Project Gutenberg, andis presented in cooperation with World Library, Inc., from theirLibrary of the Future and Shakespeare CDROMS.  Project Gutenbergoften releases Etexts that are NOT placed in the Public Domain!!Shakespeare*This Etext has certain copyright implications you should read!*<<THIS ELECTRONIC VERSION OF THE COMPLETE WORKS OF WILLIAMSHAKESPEARE IS COPYRIGHT 1990-1993 BY WORLD LIBRARY, INC., AND ISPROVIDED BY PROJECT GUTENBERG ETEXT OF ILLINOIS BENEDICTINE COLLEGEWITH PERMISSION.  ELECTRONIC AND MACHINE READABLE COPIES MAY BEDISTRIBUTED SO LONG AS SUCH COPIES (1) ARE FOR YOUR OR OTHERSPERSONAL USE ONLY, AND (2) ARE NOT DISTRIBUTED OR USEDCOMMERCIALLY.  PROHIBITED COMMERCIAL DISTRIBUTION INCLUDES BY ANYSERVICE THAT CHARGES FOR DOWNLOAD TIME OR FOR MEMBERSHIP.>>*Project Gutenberg is proud to cooperate with The World Library*in the presentation of The Complete Works of William Shakespearefor your reading for education and entertainment.  HOWEVER, THIS"
embedder = TextEmbedding()
query_embedding = embedder.get_embedding(query)

searcher = Searcher()
result_json = searcher.search(query_embedding, size=2)


print(result_json)
