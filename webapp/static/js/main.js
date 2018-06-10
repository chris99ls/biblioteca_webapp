function bookSearch(){

    var search= document.getElementById('search').value
    document.getElementById('result').innerHTML=""
    document.getElementById('detail').innerHTML=""
    console.log(search) 
    $("#detail").hide()
    $("#result").show()
    $.ajax({
        
        url:"https://www.googleapis.com/books/v1/volumes?q=" + search,
        dataType:"jsonp",

        success: function(data){
            for(i=0;i<data.items.length;i++){
                console.log(data.items[i].volumeInfo.industryIdentifiers[0].identifier)
                var isbn=data.items[i].volumeInfo.industryIdentifiers[0].identifier
                       


               result.innerHTML += "<a onClick=\"getBook("+isbn+");\" href=\"#\" class=\"mylink\">"+
                "<div class=\"card\" style=\"max-width: 128px;  margin-bottom: 15px;\" >" +
                "<img class=\"card-img-left img-responsive\" style=\"width: 128px;height: 185px;object-fit: cover;\" src=\""+data.items[i].volumeInfo.imageLinks.thumbnail+"\" alt=\"thumbnail\" >"+
                "<div class=\"card-footer\" style=\"height: 115px ;white-space: break-word;overflow: hidden;text-overflow: ellipsis;\">"+
                data.items[i].volumeInfo.title+"</div></div></a>"



            }
        },

        type:'GET'

    });
}

function getBook(isbn){
    $("#result").hide()
    $("#detail").show()
    $.ajax({
        url:"https://www.googleapis.com/books/v1/volumes?q=" + isbn,
        dataType:"jsonp",

        success: function(data){
        
            console.log("getBook:"+data.items[0].volumeInfo.industryIdentifiers[0].identifier)
            var authors=""
            for(i=0;i<data.items[0].volumeInfo.authors.length;i++){
                authors +=data.items[0].volumeInfo.authors[i]+", "
            }

            var title=data.items[0].volumeInfo.title
            var description=data.items[0].volumeInfo.description
            var isbn=data.items[0].volumeInfo.industryIdentifiers[0].identifier
            var thumbnail=data.items[0].volumeInfo.imageLinks.thumbnail

            detail.innerHTML="<div class=\"card\" style=\"padding: 50px;\"><div class=\"row \"><div class=\"col-md-3\""+
            " style=\"margin-bottom: 50px;\"><a href=\"#\" onclick=\"bookSearch();\" classs=\"btn btn-lg btn-outline-primary"+
            " text-uppercase go_back\" style=\"margin-right:20px;\"> <i class=\"fas fa-arrow-left\" style=\"margin: 5px;\"></i>"+
            "</a><img src="+thumbnail+"class=\"img-fluid\" style=\"height: 185px;width: 128px;\">"+
            "</div><div class=\"col-md-8 px-3\"><div class=\"card-block px-3\"><h3 class=\"title mb-3\">"+title+
            "</h3><dl class=\"item-property\"><dt>Author</dt><dd><p>"+authors+"</p></dd></dl><dl class=\"item-property\"><dt>Description</dt>"+
            "<dd><p>"+description+"</p></dd></dl><dl class=\"item-property\"><dt>Isbn:</dt><dd><p>"+
            isbn+"</p></dd></dl><hr><a href=\"add/"+isbn+"\" class=\"btn btn-lg btn-outline-primary"+
            " text-uppercase\"> <i class=\"fas fa-plus\" style=\"margin: 5px\"></i> Aggiungi a catalogo </a></div></div></div></div></div>"        
        },

        type:'GET'

    });
}


document.getElementById('button').addEventListener('click',bookSearch,false)
