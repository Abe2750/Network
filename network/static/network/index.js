document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll(".link").forEach(link =>
    link.addEventListener("click", (event) =>{
         
          var tag = event.target.getAttribute('id').substring(1,);
          document.getElementById("text" + tag).innerHTML = document.getElementById("post" + tag).innerHTML;
          document.getElementById("post" + tag).style.display = 'none';
          document.getElementById("form" + tag).style.display = 'block';
          

          event.preventDefault();

          document.getElementById("form" + tag).addEventListener('submit', (event) => {
              
              event.preventDefault();
              edit1(tag);
              
          });
          
    }));
    var els = document.querySelector('.like');
    if (els){
      document.querySelectorAll(".like").forEach((like =>
        like.addEventListener("click", (event)=>{
          var tag = event.target.getAttribute('id').substring(1,);
          Like(tag);
          
          
        })
   ));
    }
    
      var el = document.querySelector('#post-form');
      if (el) {

        el.addEventListener('submit', (event) => {

          event.preventDefault();
          create_post();
          // return false;
        });
      }
      
    
  
    // By default, load the inbox

    
  });
  
  function create_post() {
    fetch('/post', {
      method: 'POST',
      body: JSON.stringify({
          posttext: document.querySelector('#post-text').value,
          credentials: 'same-origin',
      })
    })
    .then(response => response.json())
    .then(result => {
        
        location.reload();
    }); 
    return false; 
}

function edit1(post1) {
  var url = '/edit/' + post1;
  fetch('/edit', {
    method: 'POST',
    body: JSON.stringify({
        post_id: post1,
        posttext: document.getElementById("text" + post1).value,
        credentials: 'same-origin',
       
    })
  })
  .then(response => response.json())
  .then(result => {
      
      
      document.getElementById("post" + result["id"]).innerHTML = result["postNote"];
      document.getElementById("post" + result["id"]).style.display = 'block';
      document.getElementById("form" + result["id"]).style.display = 'none';
  
      //location.reload();
  }); 
  return false; 
}

function Like(id) {
  
  fetch('/like', {
    method : 'POST', 
    body: JSON.stringify({
      post_id : id,
      credentials: 'same-origin',
      
    }),
  })
  .then (response => response.json()).then(
    result => {
        var id = result["id"];
        var nlikes = result["nlikes"];
        
        if (result["check"]){
          document.getElementById("like" + id).innerHTML= 
          `<p id = "like${ id }" ><a  class = "like" id = "c${id}" ><i  id = "b${id }" class=" fa fa-heart" style="font-size:18px; color: blue"></i> </a> ${nlikes}</a></p>`;
        }
        else {
          document.getElementById("like" + id).innerHTML=`<p id = "like${ id }" ><a  class = "like" id = "c${id}"><i  id = "b${id }" class=" fa fa-heart-o" style="font-size:18px; color: blue"></i> </a> ${nlikes}</a></p>`;
        }
        var x = document.getElementById("c"+id);
        x.addEventListener("click", (event)=>{
          var tag = event.target.getAttribute('id').substring(1,);
          Like(tag);
          
          
        })
        



        //location.reload();
    });
    return false;
}
