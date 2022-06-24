$( document ).ready(function() {

    fileEl = $(".fileElem")
    
    var i = 0;

    curImage =  imageList[i]


    function setImage(collection, imageName){

        curImagePath = BASE_IMAGE_PATH  + '/' + collection + '/' + imageName

        if (imageName) {
        curImagePath = BASE_IMAGE_PATH  + '/' + collection + '/' + imageName
            $(".img-name").text(imageName)
            $(".main-image").attr("src", curImagePath )
        }
    }

    function updateButtons(){

        if (i == 0) {
            $(".btn-prev").addClass('disabled');
        }
        else{
            $(".btn-prev").removeClass('disabled');
        }

        if (i < imageList.length - 1) {
            // $(".btn-yes").removeClass('disabled');
            // $(".btn-no").removeClass('disabled');
            $(".btn-skip").removeClass('disabled');
        }
        else{
           

            // $(".btn-yes").addClass('disabled');
            // $(".btn-no").addClass('disabled');
            $(".btn-skip").addClass('disabled');
        }
    }

    function moveNext(){

        if (i < imageList.length - 1){
            i = i + 1;
        }
        
        curImage =  imageList[i]
        setImage(curCollection, curImage)
        updateButtons()
    }

    
    

    $(".fileElem").on("change", function(e){
        console.log("changed")

        image_list = this.files
        for (let i = 0; i < image_list.length; i++) {
            const file = image_list[i];
            
            if (!file.type.startsWith('image/')){ continue }

            
            // const img = document.createElement("img");
            // img.classList.add("obj");
            // img.file = file;
            // preview.appendChild(img); // Assuming that "preview" is the div output where the content will be displayed.
            
            // const reader = new FileReader();
            // reader.onload = (function(aImg) { return function(e) { aImg.src = e.target.result; }; })(img);
            // reader.readAsDataURL(file);
          }

        console.log(image_list.length)
    })

    $(".fileSelect").on("click", function(e){

        e.preventDefault();

        
        if (fileEl) {
            fileEl.click();
        }
    })

    $(".btn-prev").on("click", function(e){

        e.preventDefault();

        console.log("prev")

       
        if (i > 0){
            i = i - 1;
        }

        console.log(i)
        console.log(imageList.length)
        
        curImage =  imageList[i]
        setImage(curCollection, curImage)
        updateButtons()
    })

    $(".btn-yes").on("click", function(e){

        e.preventDefault();
       
        console.log("yes")

        $(".btn-yes").addClass('active')
        $(".btn-no").removeClass('active')

        payload = {
            "image_name": curCollection + '/' + curImage,
            "tags" : ['license', 'license plate' ]
        }

        $.ajax({
            type: "POST",
            url: 'api/v1/labels/' + curCollection + '/' + curImage,
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(payload),
            success: function(result, status, xhr){
                // console.log(result)
            },
            error: function(xhr, status, error){
                // console.log(error)
            }
        })  
        
        if (i < imageList.length - 1){
            moveNext()      
        }

        
        
        // console.log(i)
        // console.log(imageList.length)
        // curImage =  imageList[i]
        // setImage(curCollection, curImage)
        // updateButtons()

    })

    $(".btn-no").on("click", function(e){

        e.preventDefault();

        console.log("no")

        $(".btn-yes").removeClass('active')
        $(".btn-no").addClass('active')

        payload = {
            "image_name": curCollection + '/' + curImage,
            "tags" : [ ]
        }

        $.ajax({
            type: "POST",
            url: 'api/v1/labels/' + curCollection + '/' + curImage,
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(payload),
            success: function(result, status, xhr){
                // console.log(result)
            },
            error: function(xhr, status, error){
                // console.log(error)
            }
        })
       
        if (i < imageList.length - 1){
            moveNext()      
        }
        // if (i < imageList.length - 1){
        //     i = i + 1;
        // }
        
        // curImage =  imageList[i]
        // setImage(curCollection, curImage)
        // updateButtons()
       
    })

    $(".btn-skip").on("click", function(e){

        e.preventDefault();

        console.log("skip")
       
        if (i < imageList.length - 1){
            moveNext()      
        }
        // if (i < imageList.length - 1){
        //     i = i + 1;
        // }
        
        // curImage =  imageList[i]
        // setImage(curCollection, curImage)
        // updateButtons()

    })

    setImage(curCollection, curImage)
    updateButtons()

});