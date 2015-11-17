/* heavily derived from
    http://alignedleft.com/tutorials/d3/making-a-bar-chart
    http://alignedleft.com/tutorials/d3/scales
    http://alignedleft.com/tutorials/d3/axes
    http://bost.ocks.org/mike/bar/3/
 */

/* width of height of bar chart
 * excluding axis
 */
var width = 600;
var height = 150;
/* padding between bars */
var barpadding = 1;
/* extra room added to x for axis */
var xpadding = 30;
/* extra room added to y for axis */
var ypadding = 40;

// get max value of dataset for scaling
var dataset_max = Math.max.apply(Math, dataset);

// scale:
// mapping all values from 0 .. dataset_max
// onto 0 .. height
var scale = d3.scale.linear()
    .domain([0, dataset_max])
    .range([0, height]);

// yaxis - commit numbers
var yaxis = d3.svg.axis()
    .scale( d3.scale.linear()
            .domain([0, dataset_max])
            .range([height, 0]) )
    .orient("right")
    .ticks(10);

/* NB:
 * domain is [inclusive, exclusive)
 * and dates in js are off by one
 * but timescale display is correct
 */
var xdates = d3.time.scale()
    .domain([
            new Date(dataset_from),
            new Date(dataset_to),
            //new Date(dataset_labels[0]),
            //new Date(dataset_labels[dataset_labels.length - 1])
    ])
    .range([0, width]);

// xaxis - labels
var xaxis = d3.svg.axis()
    .scale(xdates)
    .orient("bottom")
    .ticks(d3.time.months)
    .tickSize(16, 0)
    .tickFormat(d3.time.format("%m"));

// create SVG element
var svg = d3.select("body")
    .append("svg")
    .attr("width", width + xpadding)
    .attr("height", height + ypadding);

// draw our bars
svg.selectAll("rect")
    .data(dataset)
    .enter()
    .append("rect")
    .attr("x", function(d, i) {
        return i * (width / dataset.length);
    })
    .attr("y", function(d) {
        return height - scale(d);
    })
    .attr("width", width / dataset.length - barpadding)
    .attr("height", function(d) {
        return scale(d);
    })
    .attr("fill", function(d) {
        return "rgb(0, 0, " + (d * 10) + ")";
    })
    .attr("transform", "translate(0, " + (ypadding/4) + ")")

svg.append("g")
    .attr("class", "xaxis")
    .attr("transform", "translate(" + width + ", " + (ypadding/4) + ")")
    .call(yaxis);

svg.append("g")
    .attr("class", "axis")
    /* translate by
     * -1 * width / (dataset.length * 2)
     *  double dataset.length so we move by half a bar
     */
    .attr("transform", "translate(" + (-width/(dataset.length * 2)) + ", " + (height + ypadding/4) + ")")
    .call(xaxis);


/*
// add our labels
svg.selectAll("text")
    .data(dataset)
    .enter()
    .append("text")
    .text(function(d) {
        return d;
    })
    .attr("text-anchor", "middle")
    .attr("x", function(d, i) {
        return i * (width / dataset.length) + (width / dataset.length - barpadding) / 2;
    })
    .attr("y", function(d) {
        return height - (d * 4) + 14;
    })
    .attr("font-family", "sans-serif")
    .attr("font-size", "11px")
    .attr("fill", "white");
 */


