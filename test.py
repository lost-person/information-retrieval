

def eval_file(res):
    with open('./res_tmp.txt', 'a+') as fp:
        one_line=""
        for query_id,one_query in enumerate(res):
                i=1
                for doc_id,doc_score in zip(one_query[0],one_query[1]):
                        one_line = str(query_id+1)+" Q0 "+str(doc_id)+" "+str(i)+" "+str(doc_score)+" myrun\n"
                        fp.write(one_line) 
                        i+=1
            # print(one_line)

