const mapkit = window.mapkit;

mapkit.init({
  authorizationCallback: (done) => {
    fetch('/token')
      .then(res => res.text())
      .then(token => done(token))
      .catch(error => {});
  }
});

let url="/json";
fetch(url).then(response => response.json())
.then( (data) => {
  var rs = []
  data.map(e=>{
    const coordinate = new mapkit.Coordinate(e['lon'],e['lat']);
    const annotation = new mapkit.MarkerAnnotation(coordinate, {
      title: e['radio'],
      subtitle: e['cell'].toString(),
      color: "#0048CF",
      glyphImage: { 1: "/static/swisscom.png" },
      selectedGlyphImage: { 1: "/static/swisscom.png", 2: "/static/swisscom_2x.png", 3: "/static/swisscom_3x.png" }
    });
    rs.push(annotation)
  })
  const map = new mapkit.Map('map',{
    region : new mapkit.CoordinateRegion(new mapkit.Coordinate(data[0]['lon'],data[0]['lat']), new mapkit.CoordinateSpan(0.3, 0.3)),
    showsUserLocationControl: true,
    showsCompass: true,
    showsScale: mapkit.FeatureVisibility.Visible
  });
  rs.map(e=>{
    map.addAnnotation(e)
  })
})
