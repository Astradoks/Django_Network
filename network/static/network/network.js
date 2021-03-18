document.addEventListener("DOMContentLoaded", function() {

    // Hide all textareas
    document.querySelectorAll('#edit_post_area').forEach((textarea) => {
        textarea.style.display = 'none';
    });

    // Hide all save buttons
    document.querySelectorAll('#save_edited_post').forEach((button) => {
        button.style.display = 'none';
    });

    // Event listener for like buttons
    document.querySelectorAll(".like").forEach((button) => {
        button.addEventListener("click", (event) => {
            fetch('/like', {
                method: 'PUT',
                body: JSON.stringify({
                    id: event.target.id
                })
            })
            .then((response) => response.json())
            .then(data => {
                if (data.user_like){
                    document.getElementById(event.target.id).className = "btn btn-outline-danger btn-sm like";
                    document.getElementById(event.target.id).innerHTML = "Dislike";
                } else {
                    document.getElementById(event.target.id).className = "btn btn-outline-success btn-sm like";
                    document.getElementById(event.target.id).innerHTML = "Like";
                }
                document.getElementById(event.target.id).parentElement.childNodes[13].innerHTML = data.likes;
            });
        });
    });

    // Event listener to edit posts
    document.querySelectorAll('#edit_post').forEach((post) => {
        post.addEventListener('click', (event) => {
            // Hide all textareas
            document.querySelectorAll('#edit_post_area').forEach((textarea) => {
                textarea.style.display = 'none';
            });
            // Hide all save buttons
            document.querySelectorAll('#save_edited_post').forEach((button) => {
                button.style.display = 'none';
            });
            // Show all contents
            document.querySelectorAll('p').forEach((p) => {
                p.style.display = 'block';
            })
            // Hide content
            event.target.parentElement.childNodes[7].style.display = 'none';
            let content = event.target.parentElement.childNodes[7].innerHTML;
            // Show textarea
            event.target.parentElement.childNodes[9].style.display = 'block';
            event.target.parentElement.childNodes[9].value = content;
            // Show save button
            event.target.parentElement.childNodes[15].style.display = 'inline';
            event.target.parentElement.childNodes[15].addEventListener('click', (event) => {
                fetch('/edit', {
                    method: 'PUT',
                    body: JSON.stringify({
                        id: event.target.dataset.postid,
                        content: event.target.parentElement.childNodes[9].value
                    })
                })
                .then((response) => response.json())
                .then(data => {
                    event.target.parentElement.childNodes[15].style.display = 'none';
                    event.target.parentElement.childNodes[9].style.display = 'none';
                    event.target.parentElement.childNodes[7].style.display = 'block';
                    event.target.parentElement.childNodes[7].innerHTML = data.new_content;
                    event.target.parentElement.childNodes[20].innerHTML = data.new_time;
                });
            });
        });
    });

    // Event listener fot following buttons
    document.getElementById('follow_user').addEventListener('click', (event) => {
        fetch('/follow', {
            method: "POST",
            body: JSON.stringify({
                id: event.target.dataset.userid
            })
        })
        .then((response) => response.json())
        .then(data => {
            if (data.user_follow){
                document.getElementById(event.target.id).className = "btn btn-sm btn-outline-danger btn-block";
                document.getElementById(event.target.id).innerHTML = "Unfollow";
            } else {
                document.getElementById(event.target.id).className = "btn btn-sm btn-outline-primary btn-block";
                document.getElementById(event.target.id).innerHTML = "Follow";
            }
            document.getElementById('followers').innerHTML = `\xa0\xa0\xa0\xa0\xa0${data.followers}`;
            document.getElementById('following').innerHTML = `\xa0\xa0\xa0\xa0\xa0${data.following}`;
        });
    });

});