/**
* Build script generated by flask-assets-pipeline
*
* This script must be run through flask-assets-pipeline to work properly.
*/
import * as esbuild from 'esbuild'
import fs from 'node:fs'

let isDev = process.env.ESBUILD_DEV === "1"

// flask-assets-pipeline will provide ESBUILD_ENTRYPOINTS containing
// the entrypoints defined using bundles in your app
let entryPoints = process.env.ESBUILD_ENTRYPOINTS.split(';').map(e => {
  if (e.includes('=')) {
    let [out_, in_] = e.split('=')
    return {in: in_, out: out_}
  }
  return e;
})

let config = {
  entryPoints,
  bundle: true,
  format: "esm",
  splitting: process.env.ESBUILD_SPLITTING === "1",
  minify: !isDev,
  sourcemap: isDev,
  outdir: process.env.ESBUILD_OUTDIR,
  outbase: process.env.ESBUILD_OUTBASE,
  assetNames: "[dir]/[name]-[hash]",
  chunkNames: "[dir]/[name]-[hash]",
  entryNames: "[dir]/[name]-[hash]",
  metafile: true,
  alias: Object.fromEntries(process.env.ESBUILD_ALIASES.split(';').map(e => e.split('='))),
  external: process.env.ESBUILD_EXTERNAL.split(';'),
  plugins: [
    // add your plugins here
  ]
}

if (process.env.ESBUILD_TARGET) {
  config.target = process.env.ESBUILD_TARGET
}

if (process.env.ESBUILD_WATCH == "1") {
  let ctx = await esbuild.context({...config, plugins: [...config.plugins, {
    name: 'rebuild-notify',
    setup(build) {
      build.onEnd(result => {
        if (result.errors.length) {
          console.error('[watch] build failed')
        } else {
          if (process.env.ESBUILD_METAFILE) {
            fs.writeFileSync(process.env.ESBUILD_METAFILE, JSON.stringify(result.metafile))
          }
          console.log('[watch] build finished')
        }
      })
    },
  }]})
  await ctx.watch()
} else {
  let result = await esbuild.build(config)
  if (process.env.ESBUILD_METAFILE) {
    fs.writeFileSync(process.env.ESBUILD_METAFILE, JSON.stringify(result.metafile))
  }
}