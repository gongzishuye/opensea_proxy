#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time: 2022/6/28 3:38 下午
import json
import logging
import glob
import datetime

from flask import Flask, jsonify

from opensea_assets import assets
from opensea_collection import collection
from proxy_generator import scheduler


app = Flask(__name__)


@app.route('/opensea/assets/<owner>', methods=['POST', 'GET'])
def get_owner_assets(owner):
    try:
        full_assets = assets.get_owner_assets(owner)
    except Exception as ex:
        logging.error(ex)
        return jsonify({'code': -1})
    return jsonify({
        'data': full_assets,
        'code': 0
    })


@app.route('/opensea/asset/<contract>/<idx>', methods=['POST', 'GET'])
def get_single_asset(contract, idx):
    try:
        asset = assets.get_single_asset(contract, idx)
    except Exception as ex:
        logging.error(ex)
        return jsonify({'code': -1})
    return jsonify({
        'data': asset,
        'code': 0
    })


@app.route('/opensea/contract/<contract_addr>', methods=['POST', 'GET'])
def get_contract(contract_addr):
    try:
        contract = collection.get_contract(contract_addr)
    except Exception as ex:
        logging.error(ex)
        return jsonify({'code': -1})
    return jsonify({
        'data': contract,
        'code': 0
    })


@app.route('/opensea/collection/<slug>', methods=['POST', 'GET'])
def get_collection(slug):
    try:
        nft_collection = collection.get_collection(slug)
    except Exception as ex:
        logging.error(ex)
        return jsonify({'code': -1})
    return jsonify({
        'data': nft_collection,
        'code': 0
    })


@app.route('/opensea/stats/<slug>', methods=['POST', 'GET'])
def get_stats(slug):
    try:
        nft_stats = collection.get_stats(slug)
    except Exception as ex:
        logging.error(ex)
        return jsonify({'code': -1})
    return jsonify({
        'data': nft_stats,
        'code': 0
    })


if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    app.run(host="0.0.0.0", port=8080)
