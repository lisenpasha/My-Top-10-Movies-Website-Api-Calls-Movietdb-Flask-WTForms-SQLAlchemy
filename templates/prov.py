import requests
api_key="954087a4f935b13fdc646ef12bdf5440"
params={
     "api_key" :"954087a4f935b13fdc646ef12bdf5440",
    "query" : "Shawshank Redemption"
         }

data=requests.get("https://api.themoviedb.org/3/search/movie?",params=params).json()
results=data["results"]
# for element in results:
#     print(element)

id_params={
    "movie_id": 278,
    "api_key" :"954087a4f935b13fdc646ef12bdf5440"
}

# id_data=requests.get("https://api.themoviedb.org/3/movie/",params=id_params).json()
# print(id_data)

id_data_url=f"https://api.themoviedb.org/3/movie/{278}?api_key={api_key}"
id_data=requests.get(id_data_url).json()
print(id_data)