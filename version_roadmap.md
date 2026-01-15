- base:
    - Python + FastAPI
    - supabase (Postgres + Storage)
    - TMDB
    - ai APIs Initial version with core features
    - Basic UI/UX
    - Functions:
        - search titles from TMDB and add to media list
        - fetch basic media details when click on a title

- mvp:

---
add titles:
0.1:  搜索 -> backend -> tmdb -> 返回 -> 确认 -> 发送到后端 -> 数据库存储/更新
0.11: paste title -> ai -> send to backend -> search tmdb -> return list -> select -> send to backend -> store/update in db
beta: 搜索 -> tmdb -> return list -> select -> send to backend -> store/update in db
1.0: search multiple titles -> send multiple request to tmdb -> return list -> select multiple -> send to backend -> store/update in db
2.0: serach multiple titles -> send requests -> tmdb -> return list -> store in queue -> select one or multiple -> send to backend -> store/update in db

0.01 TODO:
- UI: change to search bar in plus button
- UI: send out search request to backend
- backend: receive search request
- backend: search tmdb api
- backend: return search result
- UI: display search result
- db: add nessesary fields in media table


0.10 TODO:
- UI: add select from search result
- UI: send selected title to backend
- backend: receive selected title
- backend: store/update title in database
