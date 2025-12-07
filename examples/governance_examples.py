"""
AgeFix Governance Protocol Examples

Examples demonstrating how to interact with AgeFix Governance protocols:
- Proposal creation and voting
- Gauge weight voting
- Validator bribes
- Governance statistics
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
# PROPOSAL MANAGEMENT EXAMPLES
# ========================================

async def create_parameter_proposal() -> str:
    """Example 1: Create a parameter change proposal"""
    try:
        result = await client.governance.create_proposal({
            'proposalType': 'parameter_change',
            'title': 'Increase Protocol Fee from 0.3% to 0.5%',
            'description': 'This proposal aims to increase protocol sustainability by raising the swap fee from 0.3% to 0.5%. Additional revenue will fund validator rewards and development.',
            'parameters': {
                'targetContract': 'DeFiProtocol',
                'function': 'setProtocolFee',
                'args': [0.5]
            },
            'ipfsHash': 'QmProposal123...',
            'votingPeriodDays': 7
        })

        print('✅ Proposal created successfully!')
        print(f'Proposal ID: {result["proposalId"]}')
        print(f'State: {result["state"]}')
        print(f'Voting Starts: {result["votingStarts"]}')
        print(f'Voting Ends: {result["votingEnds"]}')
        print(f'Quorum Required: {result["quorumRequired"]}')
        
        return result['proposalId']
    except Exception as e:
        print(f'❌ Failed to create proposal: {str(e)}')
        raise


async def create_treasury_proposal() -> str:
    """Example 2: Create a treasury spend proposal"""
    try:
        result = await client.governance.create_proposal({
            'proposalType': 'treasury_spend',
            'title': 'Fund AgeFix Mobile App Development',
            'description': 'Allocate 100,000 AGX from treasury to fund mobile app development for iOS and Android platforms. Development timeline: 6 months.',
            'parameters': {
                'recipient': '0x...developerAddress',
                'amount': 100000,
                'token': 'AGX',
                'milestones': [
                    {'description': 'UI/UX Design', 'amount': 20000},
                    {'description': 'Core Features', 'amount': 40000},
                    {'description': 'Testing & Launch', 'amount': 40000}
                ]
            },
            'votingPeriodDays': 14
        })

        print('✅ Treasury proposal created successfully!')
        print(f'Proposal ID: {result["proposalId"]}')
        
        return result['proposalId']
    except Exception as e:
        print(f'❌ Failed to create treasury proposal: {str(e)}')
        raise


async def vote_on_proposal(proposal_id: str, vote: str, reason: str = '') -> Dict:
    """Example 3: Cast vote on proposal"""
    try:
        result = await client.governance.vote({
            'proposalId': proposal_id,
            'vote': vote,  # 'for', 'against', or 'abstain'
            'reason': reason
        })

        print('✅ Vote cast successfully!')
        print(f'Voting Power: {result["votingPower"]}')
        print(f'Vote: {result["voteRecorded"]}')
        print('Updated Totals:')
        print(f'  For: {result["updatedTotals"]["forVotes"]}')
        print(f'  Against: {result["updatedTotals"]["againstVotes"]}')
        print(f'  Abstain: {result["updatedTotals"]["abstainVotes"]}')
        
        return result
    except Exception as e:
        print(f'❌ Failed to vote: {str(e)}')
        raise


async def get_proposal_details(proposal_id: str) -> Dict:
    """Example 4: Get proposal details"""
    try:
        proposal = await client.governance.get_proposal(proposal_id)

        print('📋 Proposal Details:')
        print(f'ID: {proposal["proposalId"]}')
        print(f'Title: {proposal["title"]}')
        print(f'Type: {proposal["proposalType"]}')
        print(f'State: {proposal["state"]}')
        print('\nVoting Results:')
        print(f'  For: {proposal["forVotes"]} ({proposal["passPercentage"]}%)')
        print(f'  Against: {proposal["againstVotes"]}')
        print(f'  Abstain: {proposal["abstainVotes"]}')
        print(f'  Total: {proposal["totalVotes"]}')
        print('\nStatus:')
        print(f'  Has Quorum: {"Yes" if proposal["hasQuorum"] else "No"}')
        print(f'  Will Pass: {"Yes" if proposal["willPass"] else "No"}')
        print(f'  Quorum: {proposal["quorumPercentage"]}%')
        print('\nTimeline:')
        print(f'  Created: {proposal["createdAt"]}')
        print(f'  Voting Ends: {proposal["votingEnds"]}')
        print(f'  Time Remaining: {proposal["timeRemainingSeconds"]} seconds')
        
        if proposal.get('userVote'):
            print(f'\nYour Vote: {proposal["userVote"]["vote"]}')
            print(f'Your Voting Power: {proposal["userVote"]["votingPower"]}')
        
        return proposal
    except Exception as e:
        print(f'❌ Failed to get proposal details: {str(e)}')
        raise


async def list_proposals(state: str = 'all', limit: int = 20) -> Dict:
    """Example 5: List all proposals with filters"""
    try:
        results = await client.governance.list_proposals({
            'state': state,  # 'all', 'active', 'pending', 'succeeded', 'defeated', 'executed'
            'limit': limit,
            'offset': 0
        })

        print(f'📊 Proposals ({state}): {results["totalProposals"]} total, {results["activeProposals"]} active')
        for idx, proposal in enumerate(results['proposals'], 1):
            print(f'\n{idx}. {proposal["title"]} (ID: {proposal["proposalId"]})')
            print(f'   State: {proposal["state"]}')
            print(f'   Votes: For {proposal["forVotes"]}, Against {proposal["againstVotes"]}')
            print(f'   Voting Ends: {proposal["votingEnds"]}')
            print(f'   Will Pass: {"Yes" if proposal["willPass"] else "No"}')
        
        return results
    except Exception as e:
        print(f'❌ Failed to list proposals: {str(e)}')
        raise


# ========================================
# GAUGE VOTING EXAMPLES
# ========================================

async def vote_gauge_weights(weights: Dict[str, float]) -> Dict:
    """Example 6: Vote on gauge weights"""
    try:
        result = await client.governance.vote_gauge_weights({
            'gaugeWeights': weights  # {'defi': 40, 'gaming': 30, 'nft': 20, 'governance': 10}
        })

        print('✅ Gauge weights updated successfully!')
        print(f'Voting Power Used: {result["votingPowerUsed"]}')
        print('Weights Applied:')
        for category, weight in result['weightsApplied'].items():
            print(f'  {category}: {weight}%')
        print(f'Next Epoch Starts: {result["nextEpochStarts"]}')
        
        return result
    except Exception as e:
        print(f'❌ Failed to vote on gauge weights: {str(e)}')
        raise


async def get_gauge_weights() -> Dict:
    """Example 7: Get current gauge weights"""
    try:
        weights = await client.governance.get_gauge_weights()

        print('⚖️  Current Gauge Weights:')
        print(f'Epoch: {weights["currentEpoch"]}')
        print(f'Epoch Period: {weights["epochStarts"]} → {weights["epochEnds"]}')
        print('\nGauge Distribution:')
        for gauge in weights['gaugeWeights']:
            print(f'\n{gauge["category"].upper()}:')
            print(f'  Weight: {gauge["weightPercentage"]}%')
            print(f'  Total Votes: {gauge["totalVotes"]}')
            print(f'  Emission Multiplier: {gauge["emissionMultiplier"]}x')
            print(f'  Address: {gauge["gaugeAddress"]}')
        
        return weights
    except Exception as e:
        print(f'❌ Failed to get gauge weights: {str(e)}')
        raise


async def get_user_gauge_votes() -> Dict:
    """Example 8: Get user's gauge votes"""
    try:
        votes = await client.governance.get_my_gauge_votes()

        print('🗳️  Your Gauge Votes:')
        print(f'Voting Power Used: {votes["votingPowerUsed"]}')
        print(f'Last Updated: {votes["lastUpdated"]}')
        print('\nCurrent Allocation:')
        for category, weight in votes['weights'].items():
            print(f'  {category}: {weight}%')
        
        return votes
    except Exception as e:
        print(f'❌ Failed to get gauge votes: {str(e)}')
        raise


# ========================================
# VALIDATOR BRIBE EXAMPLES
# ========================================

async def create_bribe(gauge_address: str, token: str, amount: float, duration_weeks: int) -> str:
    """Example 9: Create validator bribe"""
    try:
        result = await client.governance.create_bribe({
            'gaugeAddress': gauge_address,
            'token': token,
            'amount': amount,
            'durationWeeks': duration_weeks
        })

        print('✅ Bribe created successfully!')
        print(f'Bribe ID: {result["bribeId"]}')
        print(f'Total Amount: {result["totalAmount"]}')
        print(f'Reward Per Vote: {result["rewardPerVote"]}')
        print(f'Expires At: {result["expiresAt"]}')
        
        return result['bribeId']
    except Exception as e:
        print(f'❌ Failed to create bribe: {str(e)}')
        raise


async def get_active_bribes(gauge_address: str = None) -> Dict:
    """Example 10: Get active bribes"""
    try:
        bribes = await client.governance.get_active_bribes({
            'gaugeAddress': gauge_address
        })

        print('💰 Active Bribes:')
        for idx, bribe in enumerate(bribes['activeBribes'], 1):
            print(f'\n{idx}. Bribe ID: {bribe["bribeId"]}')
            print(f'   Gauge: {bribe["gaugeName"]}')
            print(f'   Token: {bribe["token"]}')
            print(f'   Total Amount: {bribe["totalAmount"]}')
            print(f'   Remaining: {bribe["remainingAmount"]}')
            print(f'   Reward Per Vote: {bribe["rewardPerVote"]}')
            print(f'   Expires: {bribe["expiresAt"]} ({bribe["daysRemaining"]} days)')
            print(f'   Creator: {bribe["creator"]}')
        
        return bribes
    except Exception as e:
        print(f'❌ Failed to get active bribes: {str(e)}')
        raise


async def calculate_bribe_roi(bribe_id: str, voting_power: float) -> Dict:
    """Example 11: Calculate bribe ROI"""
    try:
        roi = await client.governance.calculate_bribe_roi({
            'bribeId': bribe_id,
            'votingPower': voting_power
        })

        print('📊 Bribe ROI Calculation:')
        print(f'Voting Power: {voting_power}')
        print(f'Expected Rewards: {roi["expectedRewards"]}')
        print(f'ROI Percentage: {roi["roiPercentage"]}%')
        print(f'Duration: {roi["durationWeeks"]} weeks')
        
        return roi
    except Exception as e:
        print(f'❌ Failed to calculate ROI: {str(e)}')
        raise


# ========================================
# GOVERNANCE STATISTICS
# ========================================

async def get_governance_stats() -> Dict:
    """Example 12: Get governance statistics"""
    try:
        stats = await client.governance.get_stats()

        print('📈 Governance Statistics:')
        print('\nCURE Token:')
        print(f'  Total Locked: {stats["totalCureLocked"]}')
        print(f'  Total Supply: {stats["totalCureSupply"]}')
        print(f'  Participation Rate: {stats["participationRate"]}%')
        print('\nProposals:')
        print(f'  Active: {stats["activeProposals"]}')
        print(f'  Total: {stats["totalProposals"]}')
        print(f'  Passed: {stats["proposalsPassed"]}')
        print(f'  Defeated: {stats["proposalsDefeated"]}')
        print('\nParticipation:')
        print(f'  Total Voters: {stats["totalVoters"]}')
        print(f'  Average Quorum: {stats["averageQuorum"]}%')
        print(f'  Average Turnout: {stats["averageTurnout"]}%')
        print('\nGauge Voting:')
        print(f'  Current Epoch: {stats["currentEpoch"]}')
        print(f'  Total Gauge Votes: {stats["totalGaugeVotes"]}')
        print('\nBribes:')
        print(f'  Active Bribes: {stats["activeBribes"]}')
        print(f'  Total Bribe Value (USD): {stats["totalBribeValueUsd"]}')
        
        return stats
    except Exception as e:
        print(f'❌ Failed to get governance stats: {str(e)}')
        raise


async def get_voting_history() -> Dict:
    """Example 13: Get user voting history"""
    try:
        history = await client.governance.get_my_voting_history()

        print('📜 Your Voting History:')
        print(f'Total Votes Cast: {history["totalVotes"]}')
        print(f'Current Voting Power: {history["currentVotingPower"]}')
        print('\nRecent Votes:')
        for idx, vote in enumerate(history['recentVotes'], 1):
            print(f'\n{idx}. Proposal {vote["proposalId"]}: {vote["proposalTitle"]}')
            print(f'   Vote: {vote["vote"]}')
            print(f'   Voting Power: {vote["votingPower"]}')
            print(f'   Date: {vote["timestamp"]}')
            if vote.get('reason'):
                print(f'   Reason: {vote["reason"]}')
        
        return history
    except Exception as e:
        print(f'❌ Failed to get voting history: {str(e)}')
        raise


# ========================================
# COMPLETE GOVERNANCE WORKFLOW
# ========================================

async def complete_governance_workflow():
    """Example 14: Complete governance workflow"""
    print('🏛️  Starting Complete Governance Workflow...\n')

    try:
        # Step 1: Get governance stats
        print('Step 1: Checking governance statistics...')
        await get_governance_stats()
        print()

        # Step 2: Create parameter proposal
        print('Step 2: Creating parameter change proposal...')
        proposal_id = await create_parameter_proposal()
        print()

        # Step 3: Get proposal details
        print('Step 3: Getting proposal details...')
        await get_proposal_details(proposal_id)
        print()

        # Step 4: Cast vote
        print('Step 4: Casting vote...')
        await vote_on_proposal(proposal_id, 'for', 'This change will improve protocol sustainability')
        print()

        # Step 5: Get gauge weights
        print('Step 5: Checking current gauge weights...')
        weights = await get_gauge_weights()
        print()

        # Step 6: Vote on gauge weights
        print('Step 6: Voting on gauge weights...')
        await vote_gauge_weights({
            'defi': 40.0,
            'gaming': 30.0,
            'nft': 20.0,
            'governance': 10.0
        })
        print()

        # Step 7: Create bribe for DeFi gauge
        print('Step 7: Creating bribe for DeFi gauge...')
        defi_gauge = next(g for g in weights['gaugeWeights'] if g['category'] == 'defi')
        await create_bribe(defi_gauge['gaugeAddress'], 'AGX', 10000, 4)
        print()

        # Step 8: Check active bribes
        print('Step 8: Checking active bribes...')
        await get_active_bribes()
        print()

        # Step 9: Check voting history
        print('Step 9: Checking voting history...')
        await get_voting_history()
        print()

        print('✅ Complete governance workflow finished successfully!')
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
        
        # await complete_governance_workflow()
        # await list_proposals('active')
        # await get_gauge_weights()
        await get_governance_stats()
        
    except Exception as e:
        print(f'Error: {str(e)}')
        return 1
    
    return 0


if __name__ == '__main__':
    exit_code = asyncio.run(main())
    exit(exit_code)
