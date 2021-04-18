function initMap(){

    var options = {
        center: {lat: 17.3850, lng: 78.4867},
        zoom: 8
    };

    map = new google.maps.Map(document.getElementById("map"), options);

    function addMarker(props){       

        function geocode(){

            // var location = 'Pipeline Road Jeedimetla'
            axios.get('https://maps.googleapis.com/maps/api/geocode/json', {
                params:{
                    address: props.location,
                    key: 'AIzaSyBW6h79fYNNzye0-Q-1pxcicyeYBlg2_9A'
                }
            })
            .then(function(response){
                const marker = new google.maps.Marker({
                    position: response.data.results[0].geometry.location,
                    map:map, 
                    icon:props.imgIcon
                });
                
                if(props.imgIcon){
                    marker.setIcon(props.imgIcon);
                }
                
                if(props.content){
                    
                    const detailWindow = new google.maps.InfoWindow({
                        content:props.content
                    });
                
                    marker.addListener("mouseover", () => {
                        detailWindow.open(map, marker);
                    });
                }
            })
            .catch(function(error){
                console.log(error);
            })

            

        }  
        geocode();

    }


    addMarker({
        location:'Pipeline road Jeedimetla',
        imgIcon:"https://img.icons8.com/nolan/64/street-view.png",
        content: `<h2>Vaibhav</h2>`
    });
    
    addMarker({
        location:'rajgir',
        imgIcon:"https://img.icons8.com/nolan/64/street-view.png",
        content: `<h2>Vaibhav</h2>`
    });

}
