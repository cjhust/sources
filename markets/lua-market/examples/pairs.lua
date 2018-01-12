tbl = {"alpha", "beta", ["one"] = "uno", ["two"] = "dos"}


print("ipairs()  output:")
for key, value in ipairs(tbl) do
    print(key, value)
end


print("\n\npairs()  output:")
for key, value in pairs(tbl) do
    print(key, value)
end


