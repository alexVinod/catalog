function home(){
	$("br").remove();
	$('#content').load('/home');	
}

function about(){
	$("br").remove();
	$('#content').load('/about');
}

function login(){
	$("br").remove();
	$('#content').load('/login');
}

function logout(){
	$("br").remove();
	window.location.replace('/logout')
	var auth2 = gapi.auth2.getAuthInstance();
	auth2.signOut().then(function () {
	  console.log('User signed out.');
	});
	//$('#content').load('/logout');
}

function category(categoryName){
	$("#content").load(categoryName)
}

function AllJson(){
	$("br").remove();
	$("#content").load("/allJSON");
	$("<br/>").insertBefore("#content");
}

function ShowCategorys(){
	$("#content").load("/showAllBookShelf/JSON");
	$("#content").children().text(JSON.stringify($("#content"), undefined, 2))
	//html(JSON.stringify(data, undefined, 2))
	//JSON.stringify($("#content").text(), null, 2);
	$("<br/>").insertBefore("#content");
}

function showSingleBookShelf(bookShelf) {
	//"/showSingleBookShelf/<bookShelf>/JSON"
	console.log(bookShelf)
	$("#content").load(`${bookShelf}`)
	$("<br/>").insertBefore("#content");
}

function ShowAllBooks(bookName){
	if(bookName=== "/showAllBooks//JSON") {
		bookName="/showAllBooks/ALL/JSON";
	}		
	//console.log(bookName)
	$("#content").load(`${bookName}`)
	$("<br/>").insertBefore("#content");
}

function updateBooks(){
	console.log("Hello")
}

function deleteBook(bood_id) {
	console.log(bood_id)
}


// var pathname = window.location.pathname; // Returns path only (/path/example.html)
// var url      = window.location.href;     // Returns full URL (https://example.com/path/example.html)
// var origin   = window.location.origin;   // Returns base URL (https://example.com)