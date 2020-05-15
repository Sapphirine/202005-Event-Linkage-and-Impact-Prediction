import * as d3 from "./lib/d3.v5.min.js";
// let d3 = d3.require("d3@5");
let colors = [d3.schemeRdYlBu[3][2], d3.schemeRdYlBu[3][0]];
let curve = d3.curveStep;
let margin = { top: 20, right: 20, bottom: 30, left: 30 };
let height = 600;
let data;

d3.tsv("weather.tsv").then(function (d) {
    data = d;
});

// function getData() {
//     const parseDate = d3.timeParse("%Y%m%d");
//     const data = d3.tsvParse(await FileAttachment("./weather.tsv").text(), (d) => ({
//         date: parseDate(d.date),
//         value0: +d["New York"], // The primary value.
//         value1: +d["San Francisco"] // The secondary comparison value.
//     }));
//     data.y = "°F";
//     return data;
// }

x = d3
    .scaleTime()
    .domain(d3.extent(data, (d) => d.date))
    .range([margin.left, width - margin.right]);
y = d3
    .scaleLinear()
    .domain([
        d3.min(data, (d) => Math.min(d.value0, d.value1)),
        d3.max(data, (d) => Math.max(d.value0, d.value1)),
    ])
    .nice(5)
    .range([height - margin.bottom, margin.top]);
xAxis = (g) =>
    g
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(
            d3
                .axisBottom(x)
                .ticks(width / 80)
                .tickSizeOuter(0)
        )
        .call((g) => g.select(".domain").remove());
yAxis = (g) =>
    g
        .append("g")
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y))
        .call((g) => g.select(".domain").remove())
        .call((g) =>
            g
                .select(".tick:last-of-type text")
                .clone()
                .attr("x", 3)
                .attr("text-anchor", "start")
                .attr("font-weight", "bold")
                .text(data.y)
        );
const aboveUid = domUid("above");
const belowUid = domUid("below");

const svg = d3.create("svg").attr("viewBox", [0, 0, width, height]).datum(data);

svg.append("g").call(xAxis);

svg.append("g").call(yAxis);

svg.append("clipPath")
    .attr("id", aboveUid.id)
    .append("path")
    .attr(
        "d",
        d3
            .area()
            .curve(curve)
            .x((d) => x(d.date))
            .y0(0)
            .y1((d) => y(d.value1))
    );

svg.append("clipPath")
    .attr("id", belowUid.id)
    .append("path")
    .attr(
        "d",
        d3
            .area()
            .curve(curve)
            .x((d) => x(d.date))
            .y0(height)
            .y1((d) => y(d.value1))
    );

svg.append("path")
    .attr("clip-path", aboveUid)
    .attr("fill", colors[1])
    .attr(
        "d",
        d3
            .area()
            .curve(curve)
            .x((d) => x(d.date))
            .y0(height)
            .y1((d) => y(d.value0))
    );

svg.append("path")
    .attr("clip-path", belowUid)
    .attr("fill", colors[0])
    .attr(
        "d",
        d3
            .area()
            .curve(curve)
            .x((d) => x(d.date))
            .y0(0)
            .y1((d) => y(d.value0))
    );

svg.append("path")
    .attr("fill", "none")
    .attr("stroke", "black")
    .attr("stroke-width", 1.5)
    .attr("stroke-linejoin", "round")
    .attr("stroke-linecap", "round")
    .attr(
        "d",
        d3
            .line()
            .curve(curve)
            .x((d) => x(d.date))
            .y((d) => y(d.value0))
    );

svg.node();
