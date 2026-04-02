-- KEYS:
-- 1: games:waiting
-- 2: game_prefix ("game:")
-- 3: player_prefix ("player:")

-- ARGV:
-- 1: user_id
-- 2: new_game_id
-- 3: game_json
-- 4: ttl_seconds

local waiting_key = KEYS[1]
local game_prefix = KEYS[2]
local player_prefix = KEYS[3]

local user_id = ARGV[1]
local new_game_id = ARGV[2]
local new_game_json = ARGV[3]
local ttl = tonumber(ARGV[4])

local player_game_key = player_prefix .. user_id .. ":game"

-- Step 1: check if player already in game
local existing_game_id = redis.call("GET", player_game_key)

if existing_game_id then
    local game_key = game_prefix .. existing_game_id
    local game_json = redis.call("GET", game_key)
    return { "EXISTING", existing_game_id, game_json }
end

-- Step 2: try get waiting game
local waiting_game_id = redis.call("SPOP", waiting_key)

if waiting_game_id then

    local game_key = game_prefix .. waiting_game_id
    local game_json = redis.call("GET", game_key)

    if game_json then

        redis.call("SETEX", player_game_key, ttl, waiting_game_id)

        return { "JOINED", waiting_game_id, game_json }
    end
end

-- Step 3: create new game

local game_key = game_prefix .. new_game_id

redis.call("SETEX", game_key, ttl, new_game_json)

redis.call("SADD", waiting_key, new_game_id)

redis.call("SETEX", player_game_key, ttl, new_game_id)

return { "CREATED", new_game_id, new_game_json }
