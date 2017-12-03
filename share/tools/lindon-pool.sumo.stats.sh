#!/usr/bin/env bash
curl 'https://sumo.lindon-pool.win/api/stats' 2> /dev/null | python -c "
import sys, json;
js=json.load(sys.stdin);
print 'Pool Sumo.Lindon-Pool.win stats:'
print 'Pool HashRate {0} kH/s, at {1} miners.'.format(js['pool']['hashrate'],js['pool']['miners']);
print 'Pool Difficulty {0} , round {1} hashes.'.format(js['network']['difficulty'], js['pool']['roundHashes']);
print 'Current effort: {0}%.'.format(round(float(js['pool']['roundHashes'])/float(js['network']['difficulty'])*100,2))"
