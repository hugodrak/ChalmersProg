include("project_runner.jl")
using Latexify

println("Creating lines for latex")
println("-----ACTIVE_OUTFLOW------")
for (k, l) in node_pairs
    if active_flow[k, l] > 0
        println("\\draw[->, line width=1pt] (v$k) edge node [pos=.5, above, sloped] {$(round(active_flow[k, l], digits=4))} (v$l);")
    else
        println("\\draw[->, line width=1pt] (v$l) edge node [pos=.5, above, sloped] {$(round(active_flow[l, k], digits=4))} (v$k);")
    end
end

println("-----ACTIVE INFLOW------")
for (k, l) in node_pairs
    if active_flow[k, l] < 0
        println("\\draw[->, line width=1pt] (v$l) edge node [pos=.5, above, sloped] {$(-round(active_flow[k, l], digits=4))} (v$k);")
    else
        println("\\draw[->, line width=1pt] (v$k) edge node [pos=.5, above, sloped] {$(-round(active_flow[l, k], digits=4))} (v$l);")
    end
end

println("Creating lines for latex")
println("-----REACTIVE_OUTFLOW------")
for (k, l) in node_pairs
    if reactive_flow[k, l] > 0
        println("\\draw[->, line width=1pt] (v$k) edge node [pos=.5, above, sloped] {$(round(reactive_flow[k, l], digits=4))} (v$l);")
    else
        println("\\draw[->, line width=1pt] (v$l) edge node [pos=.5, above, sloped] {$(round(reactive_flow[l, k], digits=4))} (v$k);")
    end
end

println("-----REACTIVE INFLOW------")
for (k, l) in node_pairs
    if reactive_flow[k, l] < 0
        println("\\draw[->, line width=1pt] (v$l) edge node [pos=.5, above, sloped] {$(-round(reactive_flow[k, l], digits=4))} (v$k);")
    else
        println("\\draw[->, line width=1pt] (v$k) edge node [pos=.5, above, sloped] {$(-round(reactive_flow[l, k], digits=4))} (v$l);")
    end
end


println("----------------- Generator capacities, nodes and prices ------------------")
print(latexify(hcat(1:9, parent_node_g, W_max, C), env=:table))

println("----------------- Demand at nodes ------------------")
print(latexify(hcat(parent_node_c, D), env=:table))

println("----------------- Voltage, phase at nodes ------------------")
print(latexify(hcat(1:11, round.(JuMP.value.(v), digits=5), round.(JuMP.value.(theta), digits=5)), env=:table))

println("----------------- Power by generator nodes ------------------")
print(latexify(hcat(1:9, round.(JuMP.value.(W), digits=5)), env=:table))


println("----------------- Reactive power ------------------")
print(latexify(hcat(1:11, round.(JuMP.value.(reactive_power_constraints), digits=5)), env=:table))