document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));

  // By default, load the inbox
  load_mailbox('inbox');

   document.querySelector('#compose').addEventListener('click', compose_email);
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('form').onsubmit = function() {
    send_email();
    alert("E-mail sent succesfully");
  }
}

function send_email(){
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
.then(response => response.json())
  .then(result => {
    if (result) {
      load_mailbox('sent');
    }
    else {
       document.querySelector("#compose-view").innerHTML = "Error";
    }
  })

// avoid form from submitting
return false;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
   fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
     // email = JSON.stringify(email);
    let emailsection = document.createElement("a"); //create a clickable area
    if (mailbox == 'sent'){
      let content = `<p style="font-weight:bold;"> ${email.recipients} <span style="font-weight:normal;margin-left:50px;"> 
      Subject : ${email.subject} <br> Body: ${email.body} </span> <i style="font-weight:normal;float:right;margin-right: 40px;"> ${email.timestamp} </i> </p>`;
      emailsection.innerHTML = content; //set its content
      emailsection.setAttribute('class','emailsec'); //set its style
      document.querySelector('#emails-view').append(emailsection);
    }
    else{
    let content = `<p style="font-weight:bold;"> ${email.sender}<span style="font-weight:normal;margin-left:50px;"> 
    Subject : ${email.subject} </span> <i style="font-weight:normal;float:right;margin-right: 40px;"> ${email.timestamp} </i> </p>`;
    emailsection.innerHTML = content; //set its content
    emailsection.setAttribute('class','emailsec'); //set its style
    emailsection.href ="#"; // make it clickable
    if (email.read) {
      emailsection.style.backgroundColor = "#a5a69f"
    }
    emailsection.onclick = function (e) { // when clicked
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })
        let reply = document.createElement("button");
        let archive = document.createElement("button");    
        reply.setAttribute('class','replybutton');
        reply.innerHTML = "Reply"
        archive.setAttribute('class','archivebutton');
        let detail = document.createElement("div");
        const detailcontent =`<h1> E-mail </h1> <p style="font-weight:bold;"> Sender : ${email.sender} </p> <p style="font-weight:bold";> Recipients : ${email.recipients} <i style="font-weight:normal;float:right;margin-right: 40px;"> ${email.timestamp} </i><h6 style="margin-left:50px;color:#eb5234"> 
        Subject : ${email.subject} </h6> <hr> <p> ${email.body} </p> `;
        detail.innerHTML = detailcontent;
        detail.append(reply);
        detail.append(archive);
        document.querySelector("#emails-view").innerHTML = " ";
        document.querySelector('#emails-view').append(detail);
        if (email.archived == true ){
          archive.innerHTML = "un-Archive";
        }
        else{
          archive.innerHTML = "Archive";
        }
        archive.onclick = function () {
          archive_email(email.id,email.archived);
        }
        reply.onclick = function () {
          reply_email(email.sender,email.subject,email.body,email.timestamp);
        }
    }
  }
    document.querySelector('#emails-view').append(emailsection);
    });
}); 
}

function reply_email(sender,subject,body,time) {
  
   // Show compose view and hide other views
   document.querySelector('#emails-view').style.display = 'none';
   document.querySelector('#compose-view').style.display = 'block';
 
   // Clear out composition fields
   document.querySelector('#compose-recipients').value = sender;
   document.querySelector('#compose-subject').value = `RE: ${subject}`;
   document.querySelector('#compose-body').value = `On ${time} AM ${sender} wrote :
   
   ${body}`;
 
   document.querySelector('form').onsubmit = function() {
     const recipients = document.querySelector('#compose-recipients').value;
     const subject = document.querySelector('#compose-subject').value;
     const body = document.querySelector('#compose-body').value;
       
     fetch('/emails', {
         method: 'POST',
         body: JSON.stringify({
             recipients: recipients,
             subject: subject,
             body: body
         })
       })
     (response => response.json());
     }
 
   // avoid form from submitting
   return false;
 }
  function archive_email (id, archived) { 
    console.log(archived);
  if (archived === true){
    alert("E-mail un-archived");
    fetch( `/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    })
  }
  else {
    alert("E-mail archived");
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
      })
    })
  }
  load_mailbox('inbox');
}