"""
AgeFix NFT Marketplace Examples

Examples demonstrating how to interact with AgeFix NFT protocols:
- NFT minting
- Listing and buying
- Auctions
- NFT discovery and browsing
"""

import os
import asyncio
from typing import Dict, List, Optional
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
# NFT MINTING EXAMPLES
# ========================================

async def mint_nft(metadata: Dict) -> Dict:
    """Example 1: Mint a new NFT"""
    try:
        result = await client.nft.mint({
            'name': metadata['name'],
            'description': metadata['description'],
            'category': metadata['category'],
            'metadata': metadata['attributes'],
            'ipfsHash': metadata['ipfsHash'],
            'royaltyPercentage': metadata.get('royaltyPercentage', 5.0)
        })

        print('✅ NFT minted successfully!')
        print(f'NFT ID: {result["nftId"]}')
        print(f'Token ID: {result["tokenId"]}')
        print(f'Mint Fee (AGX): {result["mintFeeAgx"]}')
        print(f'IPFS URL: {result["ipfsUrl"]}')
        
        return result
    except Exception as e:
        print(f'❌ Failed to mint NFT: {str(e)}')
        raise


async def mint_health_certificate() -> Dict:
    """Example 2: Mint health data certificate NFT"""
    metadata = {
        'name': 'Health Data Certificate #001',
        'description': 'Verified health data contribution certificate for 365 days of activity tracking',
        'category': 'health_certificate',
        'attributes': {
            'rarity': 'rare',
            'dataPoints': 10000,
            'accuracy': 98.5,
            'durationDays': 365
        },
        'ipfsHash': 'QmXyZ123abc456def789...',
        'royaltyPercentage': 5.0
    }

    return await mint_nft(metadata)


async def mint_achievement_badge(achievement_data: Dict) -> Dict:
    """Example 3: Mint achievement badge NFT"""
    metadata = {
        'name': f'Achievement Badge: {achievement_data["name"]}',
        'description': achievement_data['description'],
        'category': 'achievement_badge',
        'attributes': {
            'rarity': achievement_data['rarity'],
            'gameId': achievement_data['gameId'],
            'unlockedAt': achievement_data['unlockedAt'],
            'playerRank': achievement_data['playerRank']
        },
        'ipfsHash': achievement_data['ipfsHash'],
        'royaltyPercentage': 2.5
    }

    return await mint_nft(metadata)


# ========================================
# MARKETPLACE LISTING EXAMPLES
# ========================================

async def list_nft_for_sale(nft_id: str, price_agx: float, duration_days: int = 7) -> str:
    """Example 4: List NFT for sale"""
    try:
        result = await client.nft.list({
            'nftId': nft_id,
            'priceAgx': price_agx,
            'listingDurationDays': duration_days
        })

        print('✅ NFT listed for sale!')
        print(f'Listing ID: {result["listingId"]}')
        print(f'Expires At: {result["expiresAt"]}')
        print(f'Marketplace Fee: {result["marketplaceFeePercentage"]}%')
        
        return result['listingId']
    except Exception as e:
        print(f'❌ Failed to list NFT: {str(e)}')
        raise


async def buy_nft(listing_id: str) -> Dict:
    """Example 5: Buy NFT from marketplace"""
    try:
        result = await client.nft.buy({
            'listingId': listing_id
        })

        print('✅ NFT purchased successfully!')
        print(f'NFT ID: {result["nftId"]}')
        print(f'Price Paid (AGX): {result["pricePaidAgx"]}')
        print(f'Marketplace Fee (AGX): {result["marketplaceFeeAgx"]}')
        print(f'Royalty Fee (AGX): {result["royaltyFeeAgx"]}')
        print(f'Seller Received (AGX): {result["sellerReceivedAgx"]}')
        
        return result
    except Exception as e:
        print(f'❌ Failed to buy NFT: {str(e)}')
        raise


async def cancel_listing(listing_id: str) -> Dict:
    """Example 6: Cancel NFT listing"""
    try:
        result = await client.nft.cancel_listing({
            'listingId': listing_id
        })

        print('✅ Listing cancelled successfully!')
        print(f'NFT ID: {result["nftId"]}')
        print(f'Refund Amount: {result["refundAmount"]}')
        
        return result
    except Exception as e:
        print(f'❌ Failed to cancel listing: {str(e)}')
        raise


# ========================================
# AUCTION EXAMPLES
# ========================================

async def create_auction(nft_id: str, starting_price: float, reserve_price: float, duration_hours: int = 48) -> str:
    """Example 7: Create auction"""
    try:
        result = await client.nft.create_auction({
            'nftId': nft_id,
            'startingPriceAgx': starting_price,
            'reservePriceAgx': reserve_price,
            'durationHours': duration_hours,
            'bidIncrementAgx': 5
        })

        print('✅ Auction created successfully!')
        print(f'Auction ID: {result["auctionId"]}')
        print(f'Ends At: {result["endsAt"]}')
        
        return result['auctionId']
    except Exception as e:
        print(f'❌ Failed to create auction: {str(e)}')
        raise


async def place_bid(auction_id: str, bid_amount: float) -> Dict:
    """Example 8: Place bid on auction"""
    try:
        result = await client.nft.place_bid({
            'auctionId': auction_id,
            'bidAmountAgx': bid_amount
        })

        print('✅ Bid placed successfully!')
        print(f'Bid Rank: {result["bidRank"]}')
        print(f'Current Highest Bid: {result["currentHighestBid"]}')
        print(f'Next Minimum Bid: {result["nextMinimumBid"]}')
        print(f'Time Remaining (seconds): {result["timeRemainingSeconds"]}')
        
        return result
    except Exception as e:
        print(f'❌ Failed to place bid: {str(e)}')
        raise


async def get_auction_details(auction_id: str) -> Dict:
    """Example 9: Get auction details"""
    try:
        auction = await client.nft.get_auction_details(auction_id)

        print('🔨 Auction Details:')
        print(f'NFT ID: {auction["nftId"]}')
        print(f'Starting Price: {auction["startingPriceAgx"]} AGX')
        print(f'Current Bid: {auction["currentBidAgx"]} AGX')
        print(f'Reserve Price: {auction["reservePriceAgx"]} AGX')
        print(f'Number of Bids: {auction["numberOfBids"]}')
        print(f'Ends At: {auction["endsAt"]}')
        print(f'Status: {auction["status"]}')
        print('\nTop Bidders:')
        for idx, bidder in enumerate(auction['topBidders'], 1):
            print(f'  {idx}. {bidder["address"][:10]}... - {bidder["bidAmount"]} AGX')
        
        return auction
    except Exception as e:
        print(f'❌ Failed to get auction details: {str(e)}')
        raise


# ========================================
# NFT DISCOVERY & BROWSING
# ========================================

async def browse_nfts(category: str, options: Optional[Dict] = None) -> Dict:
    """Example 10: Browse NFTs by category"""
    if options is None:
        options = {}
    
    try:
        results = await client.nft.browse({
            'category': category,
            'minPrice': options.get('minPrice'),
            'maxPrice': options.get('maxPrice'),
            'sort': options.get('sort', 'newest'),
            'limit': options.get('limit', 20),
            'offset': options.get('offset', 0)
        })

        print(f'🖼️  NFTs in category "{category}" ({results["totalResults"]} total):')
        for idx, nft in enumerate(results['nfts'], 1):
            print(f'\n{idx}. {nft["name"]}')
            print(f'   ID: {nft["nftId"]}')
            print(f'   Price: {nft["priceAgx"]} AGX')
            print(f'   Rarity: {nft["rarity"]}')
            print(f'   Views: {nft["views"]}, Favorites: {nft["favorites"]}')
        
        return results
    except Exception as e:
        print(f'❌ Failed to browse NFTs: {str(e)}')
        raise


async def search_nfts(keyword: str, options: Optional[Dict] = None) -> Dict:
    """Example 11: Search NFTs by keyword"""
    if options is None:
        options = {}
    
    try:
        results = await client.nft.search({
            'keyword': keyword,
            'category': options.get('category'),
            'minPrice': options.get('minPrice'),
            'maxPrice': options.get('maxPrice'),
            'limit': options.get('limit', 20)
        })

        print(f'🔍 Search results for "{keyword}" ({results["totalResults"]} found):')
        for idx, nft in enumerate(results['nfts'], 1):
            print(f'  {idx}. {nft["name"]} - {nft["priceAgx"]} AGX')
        
        return results
    except Exception as e:
        print(f'❌ Failed to search NFTs: {str(e)}')
        raise


async def get_nft_details(nft_id: str) -> Dict:
    """Example 12: Get NFT details"""
    try:
        nft = await client.nft.get_details(nft_id)

        print('🖼️  NFT Details:')
        print(f'Name: {nft["name"]}')
        print(f'Token ID: {nft["tokenId"]}')
        print(f'Description: {nft["description"]}')
        print(f'Creator: {nft["creatorAddress"]}')
        print(f'Current Owner: {nft["currentOwner"]}')
        print(f'Category: {nft["category"]}')
        print(f'Rarity: {nft["metadata"]["rarity"]}')
        print(f'Royalty: {nft["royaltyPercentage"]}%')
        print(f'Mint Date: {nft["mintDate"]}')
        print('\nAttributes:')
        for key, value in nft['metadata']['attributes'].items():
            print(f'  {key}: {value}')
        print('\nTransfer History:')
        for idx, transfer in enumerate(nft['transferHistory'], 1):
            print(f'  {idx}. {transfer["from"][:10]}... → {transfer["to"][:10]}...')
            print(f'     Price: {transfer["priceAgx"]} AGX, Date: {transfer["timestamp"]}')
        
        return nft
    except Exception as e:
        print(f'❌ Failed to get NFT details: {str(e)}')
        raise


# ========================================
# USER COLLECTION MANAGEMENT
# ========================================

async def get_user_collection() -> Dict:
    """Example 13: Get user's NFT collection"""
    try:
        collection = await client.nft.get_my_collection()

        print('🎨 My NFT Collection:')
        print(f'Total NFTs: {collection["totalNfts"]}')
        print(f'Total Value (AGX): {collection["totalValueAgx"]}')
        print('\nNFTs by Category:')
        for category, count in collection['byCategory'].items():
            print(f'  {category}: {count}')
        print('\nRecent Acquisitions:')
        for idx, nft in enumerate(collection['recentNfts'], 1):
            print(f'  {idx}. {nft["name"]} ({nft["category"]}) - Acquired: {nft["acquiredAt"]}')
        
        return collection
    except Exception as e:
        print(f'❌ Failed to get collection: {str(e)}')
        raise


async def get_ownership_history(nft_id: str) -> List[Dict]:
    """Example 14: Get NFT ownership history"""
    try:
        history = await client.nft.get_ownership_history(nft_id)

        print(f'📜 Ownership History for NFT {nft_id}:')
        for idx, record in enumerate(history, 1):
            print(f'\n{idx}. Owner: {record["owner"]}')
            print(f'   Acquired: {record["acquiredAt"]}')
            print(f'   Price: {record["priceAgx"]} AGX')
            print(f'   Duration: {record["durationDays"]} days')
        
        return history
    except Exception as e:
        print(f'❌ Failed to get ownership history: {str(e)}')
        raise


async def transfer_nft(nft_id: str, to_address: str) -> Dict:
    """Example 15: Transfer NFT to another address"""
    try:
        result = await client.nft.transfer({
            'nftId': nft_id,
            'toAddress': to_address
        })

        print('✅ NFT transferred successfully!')
        print(f'From: {result["from"]}')
        print(f'To: {result["to"]}')
        print(f'Transaction Hash: {result["txHash"]}')
        
        return result
    except Exception as e:
        print(f'❌ Failed to transfer NFT: {str(e)}')
        raise


# ========================================
# MARKETPLACE STATISTICS
# ========================================

async def get_marketplace_stats() -> Dict:
    """Example 16: Get marketplace statistics"""
    try:
        stats = await client.nft.get_marketplace_stats()

        print('📊 NFT Marketplace Statistics:')
        print(f'Total NFTs Minted: {stats["totalNftsMinted"]}')
        print(f'Total Trading Volume (AGX): {stats["totalVolumeAgx"]}')
        print(f'Active Listings: {stats["activeListings"]}')
        print(f'Active Auctions: {stats["activeAuctions"]}')
        print(f'Average Sale Price (AGX): {stats["averageSalePriceAgx"]}')
        print('\nTop Categories:')
        for idx, category in enumerate(stats['topCategories'], 1):
            print(f'  {idx}. {category["name"]}: {category["count"]} NFTs, ${category["volumeUsd"]} volume')
        print('\nTrending NFTs:')
        for idx, nft in enumerate(stats['trendingNfts'], 1):
            print(f'  {idx}. {nft["name"]} - {nft["views"]} views, {nft["sales"]} sales')
        
        return stats
    except Exception as e:
        print(f'❌ Failed to get marketplace stats: {str(e)}')
        raise


# ========================================
# COMPLETE NFT WORKFLOW
# ========================================

async def complete_nft_workflow():
    """Example 17: Complete NFT marketplace workflow"""
    print('🎨 Starting Complete NFT Workflow...\n')

    try:
        # Step 1: Mint health certificate NFT
        print('Step 1: Minting health certificate NFT...')
        mint_result = await mint_health_certificate()
        print()

        # Step 2: Get NFT details
        print('Step 2: Getting NFT details...')
        await get_nft_details(mint_result['nftId'])
        print()

        # Step 3: List NFT for sale
        print('Step 3: Listing NFT for sale...')
        listing_id = await list_nft_for_sale(mint_result['nftId'], 100, 7)
        print()

        # Step 4: Browse similar NFTs
        print('Step 4: Browsing health certificate NFTs...')
        await browse_nfts('health_certificate', {'limit': 5})
        print()

        # Step 5: Check user collection
        print('Step 5: Checking user collection...')
        await get_user_collection()
        print()

        # Step 6: Get marketplace stats
        print('Step 6: Checking marketplace statistics...')
        await get_marketplace_stats()
        print()

        print('✅ Complete NFT workflow finished successfully!')
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
        
        # await complete_nft_workflow()
        # await mint_health_certificate()
        # await browse_nfts('health_certificate')
        await get_user_collection()
        
    except Exception as e:
        print(f'Error: {str(e)}')
        return 1
    
    return 0


if __name__ == '__main__':
    exit_code = asyncio.run(main())
    exit(exit_code)
