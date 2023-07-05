# #!/usr/bin/env python
#
# import unittest
# from sql2mongo import sql_to_spec, create_mongo_shell_query, spec_str
#
#
# class TestSQLMongo(unittest.TestCase):
#     # Mark tests that will fail with 'willfail': True Most of these are for
#     # terminology that I have not writen code for.
#     test_data = [
#         {
#             'sql': """SELECT * FROM users""",
#             'mongo': """db.getCollection("users").find({}, {})""",
#         },
#         {
#             'sql': """SELECT id, user_id, status FROM users""",
#             'mongo': """db.getCollection("users").find({}, {status:1, user_id:1})""",
#         },
#         {
#             'sql': """SELECT user_id, status FROM users""",
#             'mongo': """db.getCollection("users").find({}, {_id:0, status: 1, user_id:1})""",
#         },
#         {
#             'sql': """SELECT * FROM users WHERE status = "A b" """,
#             'mongo': """db.getCollection("users").find( { status: 'A b' },{})""",
#         },
#         {
#             'sql': """SELECT user_id, status FROM users WHERE status = "A" """,
#             'mongo': """db.getCollection("users").find( { status: 'A' }, { _id:0, status: 1, user_id: 1 })""",
#         },
#         {
#             'sql': """SELECT * FROM users WHERE status != "A" """,
#             'mongo': """db.getCollection("users").find( { status: { $ne: 'A' } },{})""",
#         },
#         {
#             'sql': """SELECT * FROM users WHERE status = "A" AND age = 50""",
#             'mongo': """db.getCollection("users").find({$and:[{status:'A'}, {age: 50}]}, {})""",
#             # 'mongo': """db.getCollection("users").find( { status: 'A', age: 50 },{})""",
#         },
#         {
#             'sql': """SELECT * FROM users WHERE status = "A" OR age = 50""",
#             'mongo': """db.getCollection("users").find( { $or: [ { status: 'A' } , { age: 50 } ] }, {})""",
#         },
#         {
#             'sql': """SELECT * FROM users WHERE age > 25""",
#             'mongo': """db.getCollection("users").find( { age: { $gt: 25 } },{})""",
#         },
#         {
#             'sql': """SELECT * FROM users WHERE age < 25""",
#             'mongo': """db.getCollection("users").find( { age: { $lt: 25 } },{})""",
#         },
#         {
#             'sql': """SELECT * FROM users WHERE age > 25 AND   age <= 50""",
#             'mongo': """db.getCollection("users").find({$and:[{age:{$gt:25}}, {age:{$lte:50}}]}, {})""",
#             # 'mongo': """db.getCollection("users").find( { age: { $gt: 25, $lte: 50 } },{})""",
#         },
#         {
#             'sql': """SELECT * FROM users WHERE user_id like "%bc%" """,
#             'mongo': """db.getCollection("users").find( { user_id: {$regex:'bc'} },{})""",
#             # 'mongo': """db.getCollection("users").find( { user_id: /bc/ },{})""",
#         },
#         {
#             'sql': """SELECT * FROM users WHERE user_id like "bc%" """,
#             'mongo': """db.getCollection("users").find( { user_id: {$regex:'^bc'} },{})""",
#         },
#         {
#             'sql': """SELECT * FROM users WHERE status = "A" ORDER BY user_id ASC""",
#             'mongo': """db.getCollection("users").find( { status: 'A' } ,{}).sort( { user_id: 1 } )""",
#             'willfail': True
#         },
#         {
#             'sql': """SELECT * FROM users WHERE status = "A" ORDER BY user_id DESC""",
#             'mongo': """db.getCollection("users").find( { status: 'A' } ,{}).sort( { user_id: -1 } )""",
#             'willfail': True
#         },
#         {
#             'sql': """SELECT COUNT(*) FROM users""",
#             'mongo': """db.getCollection("users").count({})""",
#         },
#         {
#             'sql': """SELECT COUNT(user_id) FROM users""",
#             'mongo': """db.getCollection("users").count({user_id: {$exists: true}})""",
#             'willfail': True
#         },
#         {
#             'sql': """SELECT COUNT(*) FROM users WHERE age > 30""",
#             'mongo': """db.getCollection("users").count({age: {$gt: 30}})""",
#         },
#         {
#             'sql': """SELECT DISTINCT(status) FROM users""",
#             'mongo': """db.getCollection("users").distinct('status')""",
#         },
#         {
#             'sql': """SELECT * FROM users LIMIT 1""",
#             'mongo': """db.getCollection("users").find({},{}).limit(1)""",
#         },
#         {
#             'sql': """SELECT * FROM users LIMIT 5 SKIP 10""",
#             'mongo': """db.getCollection("users").find({},{}).skip(10).limit(5)""",
#         },
#         {
#             'sql': """EXPLAIN SELECT * FROM users WHERE status = "A" """,
#             'mongo': """db.getCollection("users").find( { status: 'A' },{} ).explain()""",
#         },
#         {
#             'sql': """SELECT user_id, sum(status) FROM users""",
#             'mongo': """db.getCollection("users").aggregate([{$group:{"sum(status)":{$sum:'$status'}, _id:'null'},},{$project:{"sum(status)":'$sum(status)', _id:0, user_id:1},},])""",
#         },
#         {
#             'sql': """SELECT user_id, sum(status) as status FROM users""",
#             'mongo': """db.getCollection("users").aggregate([{$group:{"sum(status)":{$sum:'$status'}, _id:'null'},},{$addFields:{"status":'$sum(status)'},},{$project:{_id:0, status:'$sum(status)', user_id:1},},])""",
#         },
#         {
#             'sql': """SELECT user_id, sum(status) as status FROM users WHERE age >= 100""",
#             'mongo': """db.getCollection("users").aggregate([{$match:{age:{$gte:100}}},{$group:{"sum(status)":{$sum:'$status'}, _id:'null'},},{$addFields:{"status":'$sum(status)'},},{$project:{_id:0, status:'$sum(status)', user_id:1},},])""",
#         },
#         {
#             'sql': """SELECT user_id, sum(status) as status FROM users WHERE age >= 100 GROUP BY user_id""",
#             'mongo': """db.getCollection("users").aggregate([{$match:{age:{$gte:100}}},{$group:{"sum(status)":{$sum:'$status'}, _id:{user_id:'$user_id'}},},{$addFields:{"status":'$sum(status)'},},{$project:{_id:0, status:'$sum(status)', user_id:'$_id.user_id'},},])""",
#         },
#         {
#             'sql': """SELECT _id, user_id, sum(status) as status FROM users WHERE age >= 100 GROUP BY _id, user_id""",
#             'mongo': """db.getCollection("users").aggregate([{$match:{age:{$gte:100}}},{$group:{"sum(status)":{$sum:'$status'}, _id:{_id:'$_id', user_id:'$user_id'}},},{$addFields:{"status":'$sum(status)'},},{$project:{_id:'$_id._id', status:'$sum(status)', user_id:'$_id.user_id'},},])""",
#         },
#     ]
#
#     def test_01_spec_str(self):
#         """
#         Convert a dictionary to mongo style.
#         """
#         input_dict = {'a': 1, "b": [{'c': 'cc'}, {'d': 0}], "e": {'f': 'g', 'h': ['i', 'j']}}
#         comp_str = "{a:1, b:[{c:'cc'}, {d:0}], e:{f:'g', h:['i', 'j']}}"
#         output_str = spec_str(input_dict)
#         assert comp_str.translate(None, " ") == output_str.translate(None, " "), \
#             "Expected {} got {} when givrn the dictionary {}".format(comp_str,
#                                                                      output_str,
#                                                                      input_dict)
#
#     def test_03_parsing(self):
#         """
#         Test is the parsing is done correctly.
#         """
#
#         for test_case in self.test_data:
#             if test_case.get('willfail'):
#                 continue
#             ret = sql_to_spec(test_case['sql'])
#             mongo_cmd = create_mongo_shell_query(ret)
#             assert test_case['mongo'].replace(" ", "") == mongo_cmd.replace(" ", ""), \
#                 "Expected {} got {} when sql is {}".format(test_case['mongo'],
#                                                            mongo_cmd,
#                                                            test_case['sql'])
#
#
# if __name__ == '__main__':
#     # 语法调整 废弃 ltw 2023-02-24
#     unittest.main()
