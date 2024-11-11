 function showAlert(){
 var username=document.getElementById('username').value;
 var first_name=document.getElementById('first_name').value;
 var password=document.getElementById('password').value;
 var password1=document.getElementById('password1').value;
 var email=document.getElementById('email').value;

 if(!username || !first_name || !email || !password || !password1){
   alert('please fill out the required filled')
  }
 else{

 alert('Registration successful.Now you can login');
  }
}
