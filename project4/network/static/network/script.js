document.addEventListener("DOMContentLoaded", function() {
    console.log("Script loaded");

    document.querySelectorAll("#postEdit").forEach(function(element) {
        element.addEventListener('click', function toggleEditHandler(e) {
            // Finds the parent Post
            let post = e.target.closest(".post");

            var body = post.querySelector("#postBody");
            let rs = post.querySelector("#rightSide");
            let ts = post.querySelector("#topPost");
            var textarea = post.querySelector("#bodyTextarea");
            var saveBtn = post.querySelector("#saveBtn");
            var editBtn = post.querySelector("#postEdit");

            if (textarea) {
                // Close textarea and revert to original content
                var originalContent = textarea.dataset.originalContent || '';
                var div = document.createElement('div');
                div.id = "postBody";
                div.innerHTML = originalContent;
                rs.replaceChild(div, textarea);
                // Revert button to "Edit"
                element.className = "fa-solid fa-pen"
                
                if (saveBtn) {
                    saveBtn.remove();
                }

                
                
            } else if (body) {
                // Open textarea for editing
                var newTextarea = document.createElement('textarea');
                newTextarea.dataset.originalContent = body.innerHTML;
                newTextarea.id = "bodyTextarea";
                newTextarea.value = body.innerHTML;
                rs.replaceChild(newTextarea, body);
                newTextarea.focus();


                // Create save button if it doesn't exist
                if (!post.querySelector("#saveBtn")) {
                    var newSaveBtn = document.createElement('button');
                    newSaveBtn.innerHTML = "Save";
                    newSaveBtn.id = "saveBtn";
                    ts.appendChild(newSaveBtn);

                    newSaveBtn.addEventListener('click', function saveHandler() {
                        let id = post.id;
                        let newContent = newTextarea.value;

                        fetch('/edit_post', {
                            method: 'POST',
                            body: JSON.stringify({
                                body: newContent,
                                id: id,
                            })
                        })

                        var newDiv = document.createElement('div');
                        newDiv.id = "postBody";
                        newDiv.innerHTML = newContent;
                        rs.replaceChild(newDiv, newTextarea);
                        newSaveBtn.remove();
                        editBtn.className = "fa-solid fa-pen"
                    });
                }

                // Change button to "Close"
                editBtn.className = "fa-solid fa-xmark"

                // Add event listener to close textarea if clicking outside
                function closeTextarea(e) {
                    if (!post.contains(e.target) && e.target !== editBtn) {
                        var textarea = post.querySelector("#bodyTextarea");
                        var saveBtn = post.querySelector("#saveBtn");
                        console.log("EWe")
                        if (textarea) {
                            var div = document.createElement('div');
                            div.id = "postBody";
                            div.innerHTML = textarea.dataset.originalContent || '';

                            rs.replaceChild(div, textarea);
                            if (saveBtn) {
                                saveBtn.remove();
                            }
                            editBtn.className = "fa-solid fa-pen"
                            editBtn.id = "postEdit";

                            // Remove the event listener to avoid multiple listeners
                            window.removeEventListener('click', closeTextarea);
                        }
                    }
                }
                window.addEventListener('click', closeTextarea);
            }
        });
    });
    // Like function
    document.querySelectorAll("#postLike").forEach(function(element) {
        element.addEventListener('click', function toggleLikeHandler(e) {
            
            let post = e.target.closest(".post");
            let postID = post.id;
            
            fetch('/like_post', {
                method: 'POST',
                body: JSON.stringify({
                    post: postID,
                })
            })
            .then(response => response.json())
            .then(data => {
                let count = post.querySelector("#postLikeCount");
                let likeBtn = post.querySelector("#likeBtn");
                let likeDiv = post.querySelector("#postLike")
                let currentCount = parseInt(count.innerHTML, 10);
                if (data.message === "Liked") {
                    console.log("Post liked");
                    // Update the UI to reflect the post has been liked
                    likeBtn.className = "fa-solid fa-heart"
                    likeDiv.className = "likeRed"


                    count.innerHTML = currentCount + 1
                } else if (data.message === "Disliked") {
                    console.log("Post disliked");
                    // Update the UI to reflect the post has been disliked
                    count.innerHTML = currentCount - 1
                    likeBtn.className = "fa-regular fa-heart"
                    likeDiv.className = "likeGray"
                    
                }


        })
    })

    })
    // Shows editBtn on post hover
    document.querySelectorAll(".post").forEach(function(element) {
        element.addEventListener("mouseover", function showEditBtn(e){
        
        
            let editBtn = element.querySelector("#postEdit");
            let saveBtn = element.querySelector("#saveBtn");
            if (editBtn){
                editBtn.style.display = "block";
                if (saveBtn){
                    saveBtn.style.display = "block";
                }
                element.addEventListener("mouseout", ()=> {
                    editBtn.style.display = "none";
                    if (saveBtn){
                        saveBtn.style.display = "none";

                    }
                } ), {once: true}
            }

        })
    })
    let postBtn = document.querySelector("#newPostBtn");
    let inputNewPost = document.querySelector("#newPostInput")
    // Change postBtn color when text in inputbox
    if (inputNewPost){
        inputNewPost.addEventListener("input", ()=> {
            if(inputNewPost.value !== "") {
                postBtn.style.background = "#1DA1F2";
                postBtn.style.color = "whitesmoke";
    
            }
            else {
                postBtn.style.background = "#045a8f";
                postBtn.style.color = "#abadb0af"
    
            }
    
        })
    }
    

    // Change color of active tab
    let allTab = document.querySelector("#allTab");
    let followingtab = document.querySelector("#followingTab");
    
    if (allTab && followingtab){
        if(window.location.href.indexOf("following") != -1){
            followingtab.style.color ="whitesmoke"
            allTab.style.textDecoration = "none";
    
        }
        else {
            allTab.style.color = "whitesmoke";
            followingtab.style.textDecoration = "none";
    
        }
    }

    

    // textarea expand

    const textarea = document.querySelector('#newPostInput');

    if (textarea){
        textarea.addEventListener('input', () => {
            console.log("#EWwe")
            textarea.style.height = 'auto';
            textarea.style.height = `${textarea.scrollHeight}px`;    
        });    
    }
    

    let editProfile = document.querySelector("#editProfile");

    if (editProfile){
        let topProfile = document.querySelector("#profileTop");
    let currentPfp = document.querySelector("#profilePfp");
    let pfpSec = document.querySelector("#pfpContainer");
    let icon = document.querySelector("#imgIcon");

    

    editProfile.addEventListener("click", function editProfileFunc(e){
        let changePfp = document.createElement("input");
        changePfp.type ="file"
        changePfp.innerHTML = "tes"
        changePfp.id = "uploadPicture"
        console.log("eww")

        if (!document.querySelector("#uploadPicture")){
            
            let icon = document.createElement("i");
            icon.className = "fa-solid fa-upload";
            icon.id = "imgIcon";
            pfpSec.appendChild(icon);
            pfpSec.appendChild(changePfp);
            
            console.log(pfpSec)
        }

        // Change pfp function
        changePfp.addEventListener("change", function uploadImage(file){
                console.log("Test")
                var input = file.target;
                var reader = new FileReader();

                reader.onload = function(){
                    var dataURL = reader.result;

                    currentPfp.src = dataURL;
                    console.log("re")

                    // Create save Btn
                    let saveImage = document.createElement("button");
                    
                    saveImage.innerHTML = "Save"
                    saveImage.id = "saveImage"

                    let editSec = document.querySelector("#editSection")
                    editSec.appendChild(saveImage);

                    editProfile.innerHTML = "Cancel";
                    editProfile.addEventListener("click", function cancel(e){
                        location.reload();
                    })

                    saveImage.addEventListener("click", function save(e){
                        fetch('/changePfp', {
                            method: 'POST',
                            body: JSON.stringify({
                                imgSrc: dataURL,
                            })
                        }).then(
                            location.reload()
                        )
                        
                    })

                };
                
                reader.readAsDataURL(input.files[0]);
                
        })
    })
    }

    

    let imageInput = document.querySelector("#imageUpload")

    if (imageInput) {

        let newPostTextarea = document.querySelector("#newPostTextarea")
        // Post with image
        imageInput.addEventListener("change", function uploadImage(file){
        console.log("Test")
        var input = file.target;
        var reader = new FileReader();

        let contentArea = document.querySelector("#contentArea")


        reader.onload = function(){
            var dataURL = reader.result;
            var image1 = document.querySelector("#image")
            if (image1){
                image1.remove()
            }
            let image = document.createElement("img")
            image.id = "image"


            let hidden = document.querySelector("#dataURL")

            contentArea.appendChild(image)

            hidden.value = dataURL;
            image.src = dataURL;
            contentArea.style.display = "flex"
            console.log(hidden)

        };
        
        reader.readAsDataURL(input.files[0]);
    })
    }
    
    

});