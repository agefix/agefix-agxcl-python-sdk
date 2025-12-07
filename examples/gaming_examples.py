"""
AgeFix Gaming Protocol Examples

Examples demonstrating how to interact with AgeFix Gaming protocols:
- Game management
- Tournaments
- Achievements
- Player statistics
"""

import os
import asyncio
from typing import Dict, List
from agxcl_sdk import AgefixClient, AgefixConfig

# Initialize client
client = AgefixClient(AgefixConfig(
    api_url='https://api.agefix.com',
    api_key=os.environ.get('AGEFIX_API_KEY'),
    network='mainnet',
    wallet_address=os.environ.get('WALLET_ADDRESS'),
    private_key=os.environ.get('PRIVATE_KEY')
))


# ========================================
# GAME MANAGEMENT EXAMPLES
# ========================================

async def register_game() -> Dict:
    """Example 1: Register a new P2E game"""
    try:
        result = await client.gaming.register_game({
            'gameName': 'AgeFix Quest',
            'gameType': 'adventure',
            'entryFeeAgx': 10,
            'rewardPoolAgx': 1000,
            'maxPlayers': 100
        })

        print('✅ Game registered successfully!')
        print(f'Game ID: {result["gameId"]}')
        print(f'Entry Fee: {result["entryFeeAgx"]} AGX')
        print(f'Reward Pool: {result["rewardPoolAgx"]} AGX')
        print(f'Status: {result["status"]}')
        
        return result
    except Exception as e:
        print(f'❌ Failed to register game: {str(e)}')
        raise


async def start_game_session(game_id: str) -> Dict:
    """Example 2: Start a new game session"""
    try:
        result = await client.gaming.start_session({
            'gameId': game_id,
            'difficulty': 'hard'
        })

        print('✅ Game session started!')
        print(f'Session ID: {result["sessionId"]}')
        print(f'Entry Fee Paid: {result["entryFeePaid"]} AGX')
        print(f'Initial Game State:')
        print(f'  Level: {result["gameState"]["level"]}')
        print(f'  Health: {result["gameState"]["health"]}')
        print(f'  Score: {result["gameState"]["score"]}')
        
        return result
    except Exception as e:
        print(f'❌ Failed to start session: {str(e)}')
        raise


async def submit_score(session_id: str, score: int, achievements: List[str]) -> Dict:
    """Example 3: Submit game score with achievements"""
    try:
        result = await client.gaming.submit_score({
            'sessionId': session_id,
            'score': score,
            'achievementIds': achievements
        })

        print('✅ Score submitted successfully!')
        print(f'Score: {result["score"]}')
        print(f'Rank: {result["rank"]}')
        print(f'Rewards Earned: {result["rewardsEarned"]} AGX')
        print(f'Achievements Unlocked: {len(result["achievementsUnlocked"])}')
        
        return result
    except Exception as e:
        print(f'❌ Failed to submit score: {str(e)}')
        raise


async def end_game_session(session_id: str, final_score: int) -> Dict:
    """Example 4: End game session and claim rewards"""
    try:
        result = await client.gaming.end_session({
            'sessionId': session_id,
            'finalScore': final_score
        })

        print('✅ Game session ended!')
        print(f'Final Score: {result["finalScore"]}')
        print(f'Total Rewards: {result["totalRewards"]} AGX')
        print(f'Duration: {result["durationMinutes"]} minutes')
        
        return result
    except Exception as e:
        print(f'❌ Failed to end session: {str(e)}')
        raise


# ========================================
# TOURNAMENT EXAMPLES
# ========================================

async def create_tournament(game_id: str) -> Dict:
    """Example 5: Create a tournament"""
    try:
        result = await client.gaming.create_tournament({
            'gameId': game_id,
            'tournamentName': 'AgeFix Championship',
            'entryFeeAgx': 50,
            'prizePoolAgx': 5000,
            'durationHours': 72,
            'maxParticipants': 100
        })

        print('✅ Tournament created successfully!')
        print(f'Tournament ID: {result["tournamentId"]}')
        print(f'Entry Fee: {result["entryFeeAgx"]} AGX')
        print(f'Prize Pool: {result["prizePoolAgx"]} AGX')
        print(f'Starts: {result["startsAt"]}')
        print(f'Ends: {result["endsAt"]}')
        
        return result
    except Exception as e:
        print(f'❌ Failed to create tournament: {str(e)}')
        raise


async def join_tournament(tournament_id: str) -> Dict:
    """Example 6: Join a tournament"""
    try:
        result = await client.gaming.join_tournament({
            'tournamentId': tournament_id
        })

        print('✅ Joined tournament successfully!')
        print(f'Tournament ID: {result["tournamentId"]}')
        print(f'Entry Fee Paid: {result["entryFeePaid"]} AGX')
        print(f'Participant Number: {result["participantNumber"]}')
        
        return result
    except Exception as e:
        print(f'❌ Failed to join tournament: {str(e)}')
        raise


async def get_tournament_leaderboard(tournament_id: str) -> Dict:
    """Example 7: Get tournament leaderboard"""
    try:
        leaderboard = await client.gaming.get_tournament_leaderboard(tournament_id)

        print('🏆 Tournament Leaderboard:')
        print(f'Tournament: {leaderboard["tournamentName"]}')
        print(f'Status: {leaderboard["status"]}')
        print(f'Total Participants: {leaderboard["totalParticipants"]}')
        print(f'Prize Pool: {leaderboard["prizePoolAgx"]} AGX')
        print(f'\nTop 10:')
        for entry in leaderboard['topPlayers']:
            print(f'  {entry["rank"]}. {entry["playerAddress"][:10]}... - Score: {entry["score"]} - Prize: {entry["prize"]} AGX')
        
        return leaderboard
    except Exception as e:
        print(f'❌ Failed to get leaderboard: {str(e)}')
        raise


async def get_tournament_details(tournament_id: str) -> Dict:
    """Example 8: Get tournament details"""
    try:
        tournament = await client.gaming.get_tournament_details(tournament_id)

        print('🎮 Tournament Details:')
        print(f'Name: {tournament["tournamentName"]}')
        print(f'Game: {tournament["gameName"]}')
        print(f'Status: {tournament["status"]}')
        print(f'Entry Fee: {tournament["entryFeeAgx"]} AGX')
        print(f'Prize Pool: {tournament["prizePoolAgx"]} AGX')
        print(f'Participants: {tournament["currentParticipants"]}/{tournament["maxParticipants"]}')
        print(f'Starts: {tournament["startsAt"]}')
        print(f'Ends: {tournament["endsAt"]}')
        
        return tournament
    except Exception as e:
        print(f'❌ Failed to get tournament details: {str(e)}')
        raise


# ========================================
# ACHIEVEMENT EXAMPLES
# ========================================

async def unlock_achievement(achievement_id: str, game_id: str) -> Dict:
    """Example 9: Unlock an achievement"""
    try:
        result = await client.gaming.unlock_achievement({
            'achievementId': achievement_id,
            'gameId': game_id
        })

        print('✅ Achievement unlocked!')
        print(f'Achievement: {result["achievementName"]}')
        print(f'Rarity: {result["rarity"]}')
        print(f'Reward: {result["rewardAgx"]} AGX')
        print(f'NFT Badge: {result["nftBadge"]}')
        
        return result
    except Exception as e:
        print(f'❌ Failed to unlock achievement: {str(e)}')
        raise


async def get_player_achievements() -> List[Dict]:
    """Example 10: Get player's achievements"""
    try:
        achievements = await client.gaming.get_player_achievements()

        print('🎖️  Your Achievements:')
        for achievement in achievements['achievements']:
            print(f'\n{achievement["name"]} ({achievement["rarity"]})')
            print(f'  Description: {achievement["description"]}')
            print(f'  Reward: {achievement["rewardAgx"]} AGX')
            print(f'  Unlocked: {achievement["unlockedAt"]}')
        
        return achievements
    except Exception as e:
        print(f'❌ Failed to get achievements: {str(e)}')
        raise


async def get_game_achievements(game_id: str) -> List[Dict]:
    """Example 11: Get all achievements for a game"""
    try:
        achievements = await client.gaming.get_game_achievements(game_id)

        print(f'🎮 Achievements for Game {game_id}:')
        for achievement in achievements['achievements']:
            print(f'\n{achievement["name"]} ({achievement["rarity"]})')
            print(f'  Description: {achievement["description"]}')
            print(f'  Reward: {achievement["rewardAgx"]} AGX')
            print(f'  Unlocked by: {achievement["unlockedByPercent"]}% of players')
        
        return achievements
    except Exception as e:
        print(f'❌ Failed to get game achievements: {str(e)}')
        raise


# ========================================
# PLAYER STATISTICS EXAMPLES
# ========================================

async def get_player_stats() -> Dict:
    """Example 12: Get player statistics"""
    try:
        stats = await client.gaming.get_player_stats()

        print('📊 Your Player Stats:')
        print(f'Total Games Played: {stats["totalGamesPlayed"]}')
        print(f'Total Earnings: {stats["totalEarningsAgx"]} AGX')
        print(f'Win Rate: {stats["winRate"]}%')
        print(f'Current Rank: {stats["currentRank"]}')
        print(f'Achievements Unlocked: {stats["achievementsUnlocked"]}')
        print(f'Tournaments Won: {stats["tournamentsWon"]}')
        print(f'Highest Score: {stats["highestScore"]}')
        
        return stats
    except Exception as e:
        print(f'❌ Failed to get player stats: {str(e)}')
        raise


async def get_global_leaderboard(limit: int = 10) -> Dict:
    """Example 13: Get global leaderboard"""
    try:
        leaderboard = await client.gaming.get_global_leaderboard({'limit': limit})

        print('🌍 Global Leaderboard:')
        for entry in leaderboard['topPlayers']:
            print(f'\n{entry["rank"]}. {entry["playerAddress"][:10]}...')
            print(f'   Earnings: {entry["totalEarningsAgx"]} AGX')
            print(f'   Win Rate: {entry["winRate"]}%')
            print(f'   Games: {entry["gamesPlayed"]}')
        
        return leaderboard
    except Exception as e:
        print(f'❌ Failed to get global leaderboard: {str(e)}')
        raise


async def get_player_ranking() -> Dict:
    """Example 14: Get player ranking details"""
    try:
        ranking = await client.gaming.get_player_ranking()

        print('📈 Your Ranking:')
        print(f'Current Tier: {ranking["currentTier"]}')
        print(f'Current Points: {ranking["currentPoints"]}')
        print(f'Next Tier: {ranking["nextTier"]}')
        print(f'Points Needed: {ranking["pointsToNextTier"]}')
        
        return ranking
    except Exception as e:
        print(f'❌ Failed to get player ranking: {str(e)}')
        raise


# ========================================
# COMPLETE GAMING WORKFLOW
# ========================================

async def complete_gaming_workflow():
    """Example 15: Complete gaming workflow"""
    print('🎮 Starting Complete Gaming Workflow...\n')

    try:
        # Step 1: Register game
        print('Step 1: Registering game...')
        game = await register_game()
        print()

        # Step 2: Start session
        print('Step 2: Starting game session...')
        session = await start_game_session(game['gameId'])
        print()

        # Step 3: Simulate gameplay
        print('Step 3: Simulating gameplay...')
        print('Playing game for 5 seconds...')
        await asyncio.sleep(5)
        print()

        # Step 4: Submit score
        print('Step 4: Submitting score...')
        await submit_score(session['sessionId'], 9500, ['first_win', 'speed_runner'])
        print()

        # Step 5: Check stats
        print('Step 5: Checking player stats...')
        await get_player_stats()
        print()

        # Step 6: Check achievements
        print('Step 6: Checking achievements...')
        await get_player_achievements()
        print()

        # Step 7: Check ranking
        print('Step 7: Checking ranking...')
        await get_player_ranking()
        print()

        print('✅ Complete gaming workflow finished successfully!')
    except Exception as e:
        print(f'❌ Workflow failed: {str(e)}')
        raise


async def complete_tournament_workflow():
    """Example 16: Complete tournament workflow"""
    print('🏆 Starting Complete Tournament Workflow...\n')

    try:
        # Step 1: Register game
        print('Step 1: Registering game...')
        game = await register_game()
        print()

        # Step 2: Create tournament
        print('Step 2: Creating tournament...')
        tournament = await create_tournament(game['gameId'])
        print()

        # Step 3: Get tournament details
        print('Step 3: Getting tournament details...')
        await get_tournament_details(tournament['tournamentId'])
        print()

        # Step 4: Join tournament
        print('Step 4: Joining tournament...')
        await join_tournament(tournament['tournamentId'])
        print()

        # Step 5: Play game
        print('Step 5: Playing tournament game...')
        session = await start_game_session(game['gameId'])
        print('Playing game for 5 seconds...')
        await asyncio.sleep(5)
        await submit_score(session['sessionId'], 9500, ['tournament_participant'])
        print()

        # Step 6: Check leaderboard
        print('Step 6: Checking tournament leaderboard...')
        await get_tournament_leaderboard(tournament['tournamentId'])
        print()

        print('✅ Complete tournament workflow finished successfully!')
    except Exception as e:
        print(f'❌ Workflow failed: {str(e)}')
        raise


# ========================================
# RUN EXAMPLES
# ========================================

async def main():
    """Main function to run examples"""
    try:
        # Uncomment the example you want to run:
        
        # await complete_gaming_workflow()
        # await complete_tournament_workflow()
        # await register_game()
        await get_player_stats()
        
    except Exception as e:
        print(f'Error: {str(e)}')
        return 1
    
    return 0


if __name__ == '__main__':
    exit_code = asyncio.run(main())
    exit(exit_code)
