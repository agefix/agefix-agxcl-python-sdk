"""
AgeFix DeFi Protocol Examples

Examples demonstrating how to interact with AgeFix DeFi protocols:
- Liquidity pool management
- Token swaps
- Lending and borrowing
- Yield farming
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
# LIQUIDITY POOL EXAMPLES
# ========================================

async def create_liquidity_pool() -> Dict:
    """Example 1: Create a new liquidity pool"""
    try:
        result = await client.defi.create_pool({
            'token0': 'AGX',
            'token1': 'CURE',
            'amount0': 100000,
            'amount1': 50000,
            'feePercentage': 0.3
        })

        print('✅ Liquidity pool created successfully!')
        print(f'Pool ID: {result["poolId"]}')
        print(f'LP Tokens Minted: {result["lpTokensMinted"]}')
        print(f'Pool Address: {result["poolAddress"]}')
        print(f'Initial K: {result["initialK"]}')
        
        return result
    except Exception as e:
        print(f'❌ Failed to create pool: {str(e)}')
        raise


async def add_liquidity(pool_id: str) -> Dict:
    """Example 2: Add liquidity to existing pool"""
    try:
        result = await client.defi.add_liquidity({
            'poolId': pool_id,
            'amount0': 1000,
            'amount1': 500,
            'slippageTolerance': 0.5
        })

        print('✅ Liquidity added successfully!')
        print(f'LP Tokens Minted: {result["lpTokensMinted"]}')
        print(f'Amount0 Added: {result["amount0Added"]}')
        print(f'Amount1 Added: {result["amount1Added"]}')
        print(f'New Pool Share: {result["poolSharePercentage"]}%')
        
        return result
    except Exception as e:
        print(f'❌ Failed to add liquidity: {str(e)}')
        raise


async def remove_liquidity(pool_id: str, lp_tokens: float) -> Dict:
    """Example 3: Remove liquidity from pool"""
    try:
        result = await client.defi.remove_liquidity({
            'poolId': pool_id,
            'lpTokens': lp_tokens
        })

        print('✅ Liquidity removed successfully!')
        print(f'Token0 Received: {result["token0Received"]}')
        print(f'Token1 Received: {result["token1Received"]}')
        print(f'LP Tokens Burned: {result["lpTokensBurned"]}')
        
        return result
    except Exception as e:
        print(f'❌ Failed to remove liquidity: {str(e)}')
        raise


# ========================================
# TOKEN SWAP EXAMPLES
# ========================================

async def get_swap_quote(pool_id: str, token_in: str, amount_in: float) -> Dict:
    """Example 4: Get swap quote before executing"""
    try:
        quote = await client.defi.get_swap_quote({
            'poolId': pool_id,
            'tokenIn': token_in,
            'amountIn': amount_in
        })

        print('💱 Swap Quote:')
        print(f'Amount In: {quote["amountIn"]} {quote["tokenIn"]}')
        print(f'Amount Out: {quote["amountOut"]} {quote["tokenOut"]}')
        print(f'Exchange Rate: {quote["exchangeRate"]}')
        print(f'Price Impact: {quote["priceImpact"]}%')
        print(f'Protocol Fee: {quote["protocolFee"]}')
        
        return quote
    except Exception as e:
        print(f'❌ Failed to get quote: {str(e)}')
        raise


async def swap_tokens(pool_id: str, token_in: str, amount_in: float, min_amount_out: float) -> Dict:
    """Example 5: Execute token swap with slippage protection"""
    try:
        result = await client.defi.swap({
            'poolId': pool_id,
            'tokenIn': token_in,
            'amountIn': amount_in,
            'minAmountOut': min_amount_out
        })

        print('✅ Swap executed successfully!')
        print(f'Amount In: {result["amountIn"]} {result["tokenIn"]}')
        print(f'Amount Out: {result["amountOut"]} {result["tokenOut"]}')
        print(f'Exchange Rate: {result["exchangeRate"]}')
        print(f'Transaction Hash: {result["txHash"]}')
        
        return result
    except Exception as e:
        print(f'❌ Failed to execute swap: {str(e)}')
        raise


# ========================================
# LENDING EXAMPLES
# ========================================

async def deposit_collateral(token: str, amount: float) -> Dict:
    """Example 6: Deposit collateral for borrowing"""
    try:
        result = await client.defi.deposit_collateral({
            'token': token,
            'amount': amount
        })

        print('✅ Collateral deposited successfully!')
        print(f'Collateral Value (USD): ${result["collateralValueUsd"]:,.2f}')
        print(f'Borrow Limit (USD): ${result["borrowLimitUsd"]:,.2f}')
        print(f'Collateral Factor: {result["collateralFactor"]}')
        
        return result
    except Exception as e:
        print(f'❌ Failed to deposit collateral: {str(e)}')
        raise


async def borrow_tokens(token: str, amount: float) -> Dict:
    """Example 7: Borrow tokens against collateral"""
    try:
        result = await client.defi.borrow({
            'token': token,
            'amount': amount
        })

        print('✅ Tokens borrowed successfully!')
        print(f'Borrowed: {result["borrowedAmount"]} {result["token"]}')
        print(f'Interest Rate APY: {result["interestRateApy"]}%')
        print(f'Health Factor: {result["healthFactor"]}')
        print(f'Liquidation Price: ${result["liquidationPrice"]}')
        
        return result
    except Exception as e:
        print(f'❌ Failed to borrow tokens: {str(e)}')
        raise


async def get_lending_position() -> Dict:
    """Example 8: Get current lending position"""
    try:
        position = await client.defi.get_lending_position()

        print('📊 Lending Position:')
        print(f'Total Collateral (USD): ${position["totalCollateralUsd"]:,.2f}')
        print(f'Total Borrowed (USD): ${position["totalBorrowedUsd"]:,.2f}')
        print(f'Available to Borrow (USD): ${position["availableToBorrowUsd"]:,.2f}')
        print(f'Health Factor: {position["healthFactor"]}')
        print(f'Liquidation Risk: {position["liquidationRisk"]}')
        
        return position
    except Exception as e:
        print(f'❌ Failed to get lending position: {str(e)}')
        raise


# ========================================
# YIELD FARMING EXAMPLES
# ========================================

async def stake_lp_tokens(pool_id: str, lp_amount: float, lock_duration_days: int = 0) -> Dict:
    """Example 9: Stake LP tokens for farming rewards"""
    try:
        result = await client.defi.stake_lp_tokens({
            'poolId': pool_id,
            'lpAmount': lp_amount,
            'lockDurationDays': lock_duration_days
        })

        print('✅ LP tokens staked successfully!')
        print(f'Stake ID: {result["stakeId"]}')
        print(f'LP Amount Staked: {result["lpAmountStaked"]}')
        print(f'Base APY: {result["baseApy"]}%')
        print(f'Lock Bonus: {result["lockBonus"]}%')
        print(f'Total APY: {result["totalApy"]}%')
        print(f'Lock Expires: {result["lockExpires"]}')
        
        return result
    except Exception as e:
        print(f'❌ Failed to stake LP tokens: {str(e)}')
        raise


async def claim_farming_rewards(stake_id: str) -> Dict:
    """Example 10: Claim accumulated farming rewards"""
    try:
        result = await client.defi.claim_farming_rewards({
            'stakeId': stake_id
        })

        print('✅ Farming rewards claimed successfully!')
        print(f'AGX Rewards: {result["agxRewards"]}')
        print(f'Value (USD): ${result["rewardsValueUsd"]:,.2f}')
        print(f'Rewards Remaining: {result["rewardsRemaining"]}')
        
        return result
    except Exception as e:
        print(f'❌ Failed to claim rewards: {str(e)}')
        raise


async def get_farming_positions() -> List[Dict]:
    """Example 11: Get all active farming positions"""
    try:
        positions = await client.defi.get_farming_positions()

        print('🌾 Active Farming Positions:')
        for idx, pos in enumerate(positions['positions'], 1):
            print(f'\n{idx}. Stake ID: {pos["stakeId"]}')
            print(f'   Pool: {pos["poolName"]}')
            print(f'   LP Staked: {pos["lpStaked"]}')
            print(f'   Value (USD): ${pos["valueUsd"]:,.2f}')
            print(f'   APY: {pos["apy"]}%')
            print(f'   Pending Rewards: {pos["pendingRewards"]} AGX')
            print(f'   Lock Expires: {pos["lockExpires"]}')
        
        return positions
    except Exception as e:
        print(f'❌ Failed to get farming positions: {str(e)}')
        raise


# ========================================
# ANALYTICS EXAMPLES
# ========================================

async def get_tvl_stats() -> Dict:
    """Example 12: Get protocol TVL statistics"""
    try:
        stats = await client.defi.get_tvl_stats()

        print('📈 Protocol TVL Statistics:')
        print(f'Total TVL (USD): ${stats["totalTvlUsd"]:,.2f}')
        print(f'Liquidity Pools TVL: ${stats["poolsTvl"]:,.2f}')
        print(f'Lending TVL: ${stats["lendingTvl"]:,.2f}')
        print(f'Farming TVL: ${stats["farmingTvl"]:,.2f}')
        print(f'\nTop Pools by TVL:')
        for pool in stats['topPoolsByTvl']:
            print(f'  {pool["name"]}: ${pool["tvl"]:,.2f}')
        print(f'\nTop Pools by Volume (24h):')
        for pool in stats['topPoolsByVolume']:
            print(f'  {pool["name"]}: ${pool["volume24h"]:,.2f}')
        
        return stats
    except Exception as e:
        print(f'❌ Failed to get TVL stats: {str(e)}')
        raise


async def get_user_portfolio() -> Dict:
    """Example 13: Get complete user DeFi portfolio"""
    try:
        portfolio = await client.defi.get_user_portfolio()

        print('💼 Your DeFi Portfolio:')
        print(f'Total Value (USD): ${portfolio["totalValueUsd"]:,.2f}')
        
        print(f'\nLiquidity Positions ({len(portfolio["liquidityPositions"])}):')
        for pos in portfolio['liquidityPositions']:
            print(f'  {pos["poolName"]}: ${pos["valueUsd"]:,.2f} ({pos["poolShare"]}% share)')
        
        print(f'\nLending Positions:')
        print(f'  Collateral: ${portfolio["lendingPosition"]["collateralUsd"]:,.2f}')
        print(f'  Borrowed: ${portfolio["lendingPosition"]["borrowedUsd"]:,.2f}')
        print(f'  Health Factor: {portfolio["lendingPosition"]["healthFactor"]}')
        
        print(f'\nFarming Positions ({len(portfolio["farmingPositions"])}):')
        for pos in portfolio['farmingPositions']:
            print(f'  {pos["poolName"]}: ${pos["stakedValueUsd"]:,.2f} @ {pos["apy"]}% APY')
        
        return portfolio
    except Exception as e:
        print(f'❌ Failed to get portfolio: {str(e)}')
        raise


# ========================================
# COMPLETE DEFI WORKFLOW
# ========================================

async def complete_defi_workflow():
    """Example 14: Complete DeFi workflow from pool creation to farming"""
    print('🚀 Starting Complete DeFi Workflow...\n')

    try:
        # Step 1: Create liquidity pool
        print('Step 1: Creating liquidity pool...')
        pool = await create_liquidity_pool()
        print()

        # Step 2: Check TVL stats
        print('Step 2: Checking protocol TVL...')
        await get_tvl_stats()
        print()

        # Step 3: Get swap quote
        print('Step 3: Getting swap quote...')
        quote = await get_swap_quote(pool['poolId'], 'AGX', 100)
        print()

        # Step 4: Execute swap
        print('Step 4: Executing token swap...')
        await swap_tokens(pool['poolId'], 'AGX', 100, quote['amountOut'] * 0.99)
        print()

        # Step 5: Add more liquidity
        print('Step 5: Adding more liquidity...')
        await add_liquidity(pool['poolId'])
        print()

        # Step 6: Stake LP tokens
        print('Step 6: Staking LP tokens for farming...')
        stake = await stake_lp_tokens(pool['poolId'], 1000, 90)
        print()

        # Step 7: Check portfolio
        print('Step 7: Checking complete portfolio...')
        await get_user_portfolio()
        print()

        print('✅ Complete DeFi workflow finished successfully!')
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
        
        # await complete_defi_workflow()
        # await create_liquidity_pool()
        # await get_tvl_stats()
        await get_user_portfolio()
        
    except Exception as e:
        print(f'Error: {str(e)}')
        return 1
    
    return 0


if __name__ == '__main__':
    exit_code = asyncio.run(main())
    exit(exit_code)
