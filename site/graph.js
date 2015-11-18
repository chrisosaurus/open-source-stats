/* heavily derived from
    http://alignedleft.com/tutorials/d3/making-a-bar-chart
    http://alignedleft.com/tutorials/d3/scales
    http://alignedleft.com/tutorials/d3/axes
    http://bost.ocks.org/mike/bar/3/
 */

/* room for title */
var title_height = 20;
/* padding below title */
var title_padding = 20;

/* width of height of bar chart
 * excluding axis
 */
var width = 600;
var height = 150 + title_height + title_padding;
/* padding between bars */
var bar_padding = 1;
/* extra room added to x for axis */
var xpadding = 40;
/* extra room added to y for axis */
var ypadding = 40 + title_height + title_padding;

/* FIXME we need to decide on these colour graduations
 * the idea is:
 *     colour_range[0] is for  0 ..  9 %
 *     colour_range[1] is for 10 .. 19 %
 *     colour_range[2] is for 20 .. 29 %
 *     ...
 *     colour_range[8] is for 80 .. 89 %
 *     colour_range[9] is for 90 ..100 %
 */
var colour_range = [
    /* 0 =  0 ..   9 % */
    [  0, 191, 255],

    /* 1 = 10 ..  19 % */
    [  0, 154, 205],

    /* 2 = 20 ..  29 % */
    [ 30, 144, 255],

    /* 3 = 30 ..  39 % */
    [ 24, 116, 205],

    /* 4 = 40 ..  49 % */
    [ 72, 118, 255],

    /* 5 = 50 ..  59 % */
    [ 58,  95, 205],

    /* 6 = 60 ..  69 % */
    [ 16,  78, 139],

    /* 7 = 70 ..  79 % */
    [ 39,  64, 139],

    /* 8 = 80 ..  89 % */
    // FIXME this is my favourite colour
    // so I want things around this
    [  0,   0, 255],

    /* 9 = 90 .. 100 % */
    [ 25,  25, 112],
];
// default colour should never actually be used
var colour_default = [0, 0, 0];
// ongoing colour is for the current month, to show that the number is not yet final
var colour_ongoing = [138, 43, 226];

function get_colour(percent){
    var index = Math.floor(colour_range.length * percent);
    index = Math.max(index, 0);
    index = Math.min(index, (colour_range.length-1));

    if( index in colour_range ){
        return colour_range[index];
    }

    return colour_default;
}

console.log(datasets);

// draw dataset graphs
for (index in datasets){
    dataset = datasets[index]
    var project_name = dataset["project"]
    var date_from = dataset["date_from"]
    var date_to = dataset["date_to"]
    var data = dataset["data"]
    var data_len = data.length;

    console.log(dataset)
    console.log(project_name)
    console.log(date_from)
    console.log(date_to)
    console.log(data)

    // get max value of data for scaling and colouring
    var data_max = Math.max.apply(Math, data);
    // get min value of data for colouring
    var data_min = Math.min.apply(Math, data);
    var data_range = data_max - data_min;
    console.log(data_max);
    console.log(data_min);
    console.log(data_range);

    // scale:
    // mapping all values from 0 .. data_max
    // onto 0 .. height
    var scale = d3.scale.linear()
        .domain([0, data_max]).nice()
        .range([0, height]);

    // yaxis - commit numbers
    var yaxis = d3.svg.axis()
        .scale( d3.scale.linear()
                .domain([0, data_max]).nice()
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
                new Date(date_from),
                new Date(date_to),
                //new Date(data_labels[0]),
                //new Date(data_labels[data_labels.length - 1])
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

    // add a title
    svg.append("text")
        .attr("x", (width / 2))
        .attr("y", title_height)
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .text(project_name)

    var i = 0;

    // draw our bars
    svg.selectAll("rect")
        .data(data)
        .enter()
        .append("rect")
        .attr("x", function(d, i) {
            return i * (width / data_len);
        })
        .attr("y", function(d) {
            return height - scale(d) + title_padding;
        })
        .attr("width", width / data_len - bar_padding)
        .attr("height", function(d) {
            return scale(d);
        })
        .attr("fill", function(d) {
            i += 1;
            // we want to colour based on it being a percentage of the max
            // we also want to colour the final bar to indicate it being in progress

            var colour = colour_default;

            if( i == data_len ){
                // if this is the final item, then use ongoing colour
                colour = colour_ongoing;
            } else {
                // otherwise colour based on %
                var percent = (d-data_min) / data_range;
                colour = get_colour(percent);
            }
            var r = colour[0];
            var g = colour[1];
            var b = colour[2];
            return "rgb(" + r + "," + g + "," + b + ")";
        })
        .attr("transform", "translate(0, " + (ypadding/4) + ")")

    // yaxis
    svg.append("g")
        .attr("class", "xaxis")
        .attr("transform", "translate(" + width + ", " + (title_padding + ypadding/4) + ")")
        .call(yaxis);

    // yaxis label
    /*
    svg.append("text")
        .attr("class", "y label")
        .attr("text-anchor", "end")
        //.attr("y", height/2)
        //.attr("x", width)
        .attr("dy", ".75em")
        //.attr("transform", "rotate(-90)")
        .attr("transform", "translate(" + width + ", " + (title_padding + ypadding) + ") rotate(-90)")
        .text("commits");
    */

    // xaxis
    svg.append("g")
        .attr("class", "axis")
        /* translate by
         * -1 * width / (data.length * 2)
         *  double data.length so we move by half a bar
         */
        .attr("transform", "translate(" + (-width/(data_len*2)) + ", " + (height + title_padding + ypadding/4) + ")")
        .call(xaxis);

    // xaxis label
    /*
    svg.append("text")
        .attr("class", "x label")
        .attr("text-anchor", "end")
        .attr("x", width/2)
        .attr("y", height + 60)
        .text("months");
    */

}

