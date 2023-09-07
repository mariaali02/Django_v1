
function getalldata() {
    var baseUrl = "http://127.0.0.1:8000/apitest/userdetail";
    $.ajax({
        method: 'GET',
        url: baseUrl,
        dataType: "json",
        data: { },
        error: function (xhr, errmsg, err) {
            console.log('Error:', err);
        },
        complete: function (xhr, errmsg, err) {
    
            console.log('JSON Data:', xhr.responseJSON);
        },
        success: function (xhr, errmsg, err) {
            console.log('Success:', xhr);
            $('tbody#tblmydata').children().remove();
            var role = xhr.role;


            for (i=0; i < xhr.data.length; i++){
                const userData = xhr.data[i];
                var datarow = ''
                if (role)
                {
                    datarow = `<tr>
                    <td>${userData.userId}</td>
                    <td>${ userData.username }</td>
                    <td>${ userData.email }</td>
                    <td> ${ userData.date_of_birth}</td>
                    <td> ${ userData.gender }</td>
                    <td> ${ userData.phone_number}</td>   
                    <td><button onclick="deleteUser(${userData.userId})">Delete</button>
                    <button onclick="ShowUpdateView(${userData.userId})">Edit</button></td>
                    </tr>` 
                }
                else
                {
                    datarow = `<tr>
                    <td>${userData.userId}</td>
                    <td>${ userData.username }</td>
                    <td>${ userData.email }</td>
                    <td> ${ userData.date_of_birth}</td>
                    <td> ${ userData.gender }</td>
                    <td> ${ userData.phone_number}</td>
                    </tr>` 
                }
                $('tbody#tblmydata').append(datarow)
            }
        },
    });
}

//REMOVE//
function removedata() {
    alert('empty');
    $('tbody#tblmydata').empty()
}

//DELETE//
function deleteUser(userId) {
    const csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

    var baseUrl = "http://127.0.0.1:8000/apitest/SoftDeleteUser";
    var url = `${baseUrl}?userId=${userId}`;

    $.ajax({
        method: 'DELETE',
        url: url,
        success: function (data) {
            console.log(data.message);
            getalldata();
            // You can perform additional actions here after successful deletion
        },
        error: function (xhr, errmsg, err) {
            alert('Failed to delete user: ');
        }
    });
}                 

    // GET DATA BY ID//
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const addInput = document.querySelector('#addInput');
    const addBtn = document.querySelector('#addBtn');

    function getdata(userId) {
        var baseUrl = "http://127.0.0.1:8000/apitest/userdetail";
        $.ajax({
            method: 'GET',
            url: baseUrl,
            dataType: "json",
            data: { "userId": userId },
            error: function (xhr, errmsg, err) {
                console.log('Error:', err);
            },
            complete: function (xhr, errmsg, err) {

                const userData = xhr.responseJSON.data;
                $('input#txtUserName').val(userData.user);
                $('input#txtEmail').val(userData.email);
                $('input#txtdob').val(userData.date_of_birth);
                $('input#lblUserId').val(userId);
                $('input#txtEmail').val(userData.email);
                $('input#txtPhone').val(userData.phone_number); // Assuming the ID for the Phone Number input is 'txtPhone'
                $('select#selGender').val(userData.gender); // Assuming the ID for the Gender select is 'selGender'
                console.log('JSON Data:', userData);

            },
            success: function (xhr, errmsg, err) {
                console.log('Success:', xhr);
            },
        });
    }
                                                            //UPDATE DATA *PUT* //
    function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        function updateUser() {
            var csrftokenget = getCookie('csrftoken');
            formValidation();

                $.ajaxSetup({
                    beforeSend: function (xhr, settings) {
                        xhr.setRequestHeader("X-CSRFToken", csrftokenget);
                    }
                });
            
            var baseUrl = "http://127.0.0.1:8000/apitest/userdetail"; // Base URL of your Django API
            var userId = $('input#lblUserId').val()
            var email = $('input#txtEmail').val()
            var username = $('input#txtUserName').val()
            var date_of_birth = $('input#txtdob').val()
            var gender = $('select#selGender').val()
            var phone_number = $('input#txtPhone').val()
            var Url = baseUrl + `?userId=${userId}` ;

            $.ajax({
                method: 'PUT',
                url: Url, // Use the 'Url' variable containing the complete URL
                dataType: 'application/json',
                data:{'email' : email,
                'username':username,
                'date_of_birth':date_of_birth,
                'gender':gender,
                'phone_number':phone_number
            },
                dataType: 'json',
                complete: function(xhr, errmsg, err){
                /* $('input#txtUserName').val(xhr.responseJSON[0]["username"])
                    $('input#txtEmail').val(xhr.responseJSON[0]["email"])
                    $('input#lblUserId').val(xhr.responseJSON[0]["id"])
                    $('input#txtdob').val(xhr.responseJSON[0]["dob"])*/
                
                    alert('User updated successfully!');
                },
                success:  function(xhr, errmsg, err){},
                
            })
        } 
    
    function formValidation() {
        var username = document.getElementById("txtUserName").value;
        var email = document.getElementById("txtEmail").value;
        var usernameError = document.getElementById("username-error");
        var emailError = document.getElementById("email-error");
    
        usernameError.innerHTML = "";
        emailError.innerHTML = "";
    
        var usernamePattern = /^[a-zA-Z0-9_]+$/;
        var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    
        if (username.trim() === "" || username.match(usernamePattern)) {
            if (email.trim() === "" || email.match(emailPattern)) {
                return true; // Form can be submitted
            } else {
                emailError.innerHTML = "Please enter a valid email.";
                return false; // Prevent form submission due to invalid email
            }
        } else {
            usernameError.innerHTML = "INVALID";
            return false; // Prevent form submission due to invalid username
        }
    }
    
    function ShowUpdateView(userId) {
        document.getElementById('divUpdateForm').style.display = 'block';
        getdata(userId);
        
    }
                                                                    //CHECK BOXES//
    function toggleCheckbox(checkbox) {
        const selectAllCheckbox = document.querySelector('#selectAllCheckbox');
        const userCheckboxes = document.querySelectorAll('input[name="userCheckbox"]');

        if (!checkbox.checked) {
            selectAllCheckbox.checked = false;userId
        } else {
            const allChecked = Array.from(userCheckboxes).every(function (checkbox) {
                return checkbox.checked;
            });

            selectAllCheckbox.checked = allChecked;
        }
    }
// Get the modal
        var modal = document.getElementById('dlt');

// When the user clicks anywhere outside of the modal, close it
            window.onclick = function(event) {
                    if (event.target == modal) {
                    modal.style.display = "none";

    }
    }

                                                                //LOAD FUNCTION//

    // window.onload= function(){
    //     getalldata();
    // } 


                                                                //USER LOGOUT //
    function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

    function userLogout() {
        var csrftokenget = getCookie('csrftoken'); // Get CSRF token
        var baseUrl = "http://127.0.0.1:8000/apitest/SignOut/"; // Update the URL
        
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftokenget);
            }
        });

        $.ajax({
            method: 'POST',
            url: baseUrl,
            dataType: 'json',
            success: function(data) {
                alert("Successfully logged out.");
                window.location.href = data.url;
            },
            error: function(xhr, status, error) {
                alert("Logout failed. Please try again.");
                
            }
        });
    }
