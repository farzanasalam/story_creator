# story_creator
Building a Story Generator API

Technologies : FastAPI ,Supabase ,Openai API

Create character :
curl -X POST "http://127.0.0.1:8000/api/create_character" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Bilbo Baggins",
           "details": "Hobbit lives in the Shire owning a magic ring"
         }'

Generate story:
curl -X POST "http://127.0.0.1:8000/api/generate_story" \
     -H "Content-Type: application/json" \
     -d '{
           "character_name": "Bilbo Baggins"
         }'

